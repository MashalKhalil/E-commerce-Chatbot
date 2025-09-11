import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from config import Config as AppConfig
from flask import current_app
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from models.chat_session import ChatSession
from models.message import Message
from models.product import Product

from .cart_service import CartService
from .product_service import ProductService
from .vector_service import VectorService

logger = logging.getLogger(__name__)

class ChatService:
    """Enhanced chat service with LangChain and Gemini integration"""

    def __init__(self):
        self.llm = None
        self.vector_service = VectorService()
        self.product_service = ProductService()
        self.cart_service = CartService()
        self.memory_sessions = {}
        self.initialized = False

    def initialize(self):
        """Initialize LangChain components"""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=current_app.config["GOOGLE_API_KEY"],
                temperature=0.7,
                max_tokens=1000,
                convert_system_message_to_human=True,
            )
            self.vector_service.initialize()
            self.initialized = True
            logger.info("Chat service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize chat service: {str(e)}")
            raise

    def get_or_create_memory(self, session_id: str) -> ConversationBufferWindowMemory:
        """Get or create memory for a chat session"""
        if session_id not in self.memory_sessions:
            self.memory_sessions[session_id] = ConversationBufferWindowMemory(
                k=10, return_messages=True, memory_key="chat_history"
            )
        return self.memory_sessions[session_id]

    def create_tools(self) -> List[Tool]:
        """Create tools for the LangChain agent"""
        tools = [
            Tool(
                name="search_products",
                description="Find products using semantic search. Input: search query (str).",
                func=self._search_products_tool,
            ),
            Tool(
                name="filter_products",
                description="Filter products. Input: JSON string with keys: category, subcategory, brand, min_price, max_price, min_rating, in_stock_only, features (list), search_query, limit.",
                func=self._filter_products_tool,
            ),
            Tool(
                name="get_product_details",
                description="Get product details. Input: product ID (str).",
                func=self._get_product_details_tool,
            ),
            Tool(
                name="get_recommendations",
                description="Get recommendations. Input: product ID (str) or preference description (str).",
                func=self._get_recommendations_tool,
            ),
            Tool(
                name="add_to_cart",
                description="Add a product to the user's cart. Input: JSON string with keys: product_id (str or product name), quantity (int, optional, default 1).",
                func=self._add_to_cart_tool,
            ),
        ]
        return tools

    def _search_products_tool(self, query: str) -> str:
        """Tool function for semantic product search"""
        try:
            similar_products = self.vector_service.search_similar_products(query, top_k=6)
            logger.info(f"Found {len(similar_products)} similar products for query: {query}")

            if not similar_products:
                return json.dumps({"message": "No products found for the given query.", "product_ids": []})

            product_ids = [p["id"] for p in similar_products]
            products = [Product(**doc) for doc in AppConfig.db["products"].find({"id": {"$in": product_ids}})]
            if not products:
                return json.dumps({"message": "No matching products found in database.", "product_ids": []})

            result = "Found the following products:\n"
            for product in products:
                result += f"- {product.name} by {product.brand} - ${product.price}\n"
                result += f"  {product.description[:100]}...\n"

            return json.dumps({"message": result, "product_ids": product_ids})
        except Exception as e:
            logger.error(f"Error in search_products_tool: {str(e)}")
            return json.dumps({"message": "Error occurred while searching for products.", "product_ids": []})

    def _filter_products_tool(self, filter_json: str) -> str:
        """Tool function for filtering products"""
        try:
            filters = json.loads(filter_json)
            query = {}
            if "category" in filters:
                query["category"] = filters["category"]
            if "min_price" in filters and filters["min_price"]:
                query["price"] = {"$gte": float(filters["min_price"])}
            if "max_price" in filters and filters["max_price"]:
                query["price"] = query.get("price", {}) | {"$lte": float(filters["max_price"])}

            products = [Product(**doc) for doc in AppConfig.db["products"].find(query)] if query else [Product(**doc) for doc in AppConfig.db["products"].find()]
            if not products:
                return json.dumps({"message": "No products found matching the specified filters.", "product_ids": []})

            result = f"Found {len(products)} products matching your criteria:\n"
            for product in products[:5]:
                result += f"- {product.name} by {product.brand} - ${product.price}\n"

            product_ids = [product.id for product in products[:5]]
            return json.dumps({"message": result, "product_ids": product_ids})
        except Exception as e:
            logger.error(f"Error in filter_products_tool: {str(e)}")
            return json.dumps({"message": "Error occurred while filtering products.", "product_ids": []})

    def _get_product_details_tool(self, product_id: str) -> str:
        """Tool function for getting product details"""
        try:
            product_data = AppConfig.db["products"].find_one({"id": product_id.strip()})
            if not product_data:
                return "Product not found."
            product = Product(**product_data)
            result = "Product Details:\n"
            result += f"Name: {product.name}\n"
            result += f"Brand: {product.brand}\n"
            result += f"Price: ${product.price}\n"
            result += f"Rating: {product.rating}/5 ({product.review_count} reviews)\n"
            result += f"Description: {product.description}\n"
            result += f"Features: {', '.join(product.get_features())}\n"
            result += f"Stock: {product.stock} available\n"
            return result
        except Exception as e:
            logger.error(f"Error in get_product_details_tool: {str(e)}")
            return "Error occurred while getting product details."

    def _get_recommendations_tool(self, input_text: str) -> str:
        """Tool function for getting product recommendations"""
        try:
            product_data = AppConfig.db["products"].find_one({"id": input_text.strip()})
            if product_data:
                product = Product(**product_data)
                similar_products = self.vector_service.search_similar_products(product.get_search_text(), top_k=4)
                similar_ids = [p["id"] for p in similar_products if p["id"] != product.id]
            else:
                similar_products = self.vector_service.search_similar_products(input_text, top_k=4)
                similar_ids = [p["id"] for p in similar_products]

            recommendations = [Product(**doc) for doc in AppConfig.db["products"].find({"id": {"$in": similar_ids}})]
            if not recommendations:
                return "No recommendations found."
            result = "Here are some recommendations:\n"
            for rec in recommendations:
                result += f"- {rec.name} by {rec.brand} - ${rec.price}\n"
            return result
        except Exception as e:
            logger.error(f"Error in get_recommendations_tool: {str(e)}")
            return "Error occurred while getting recommendations."

    def _add_to_cart_tool(self, input_json: str) -> str:
        """Tool function to add a product to the user's cart"""
        try:
            logger.info(f"add_to_cart_tool input: {input_json}")
            data = json.loads(input_json)
            product_id = data.get("product_id")
            quantity = data.get("quantity", 1)
            user_id = data.get("user_id", "guest_user")
            logger.info(f"Parsed data: product_id={product_id}, quantity={quantity}, user_id={user_id}")

            if not product_id:
                return json.dumps({"message": "Missing product_id for add to cart.", "success": False})

            if len(product_id) < 32 or " " in product_id:
                logger.info(f"Searching for product by name: {product_id}")
                product = next((p for p in [Product(**doc) for doc in AppConfig.db["products"].find()] if product_id.lower() in p.name.lower()), None)
                if product:
                    logger.info(f"Found product: {product.name} with ID: {product.id}")
                    product_id = product.id
                else:
                    logger.warning(f"Product not found: {product_id}")
                    return json.dumps({"message": f"Product '{product_id}' not found.", "success": False})

            logger.info(f"Adding to cart: user_id={user_id}, product_id={product_id}, quantity={quantity}")
            result = self.cart_service.add_to_cart(user_id, product_id, quantity)
            logger.info(f"Cart service result: {result}")

            if not result.get("success", True):
                return json.dumps(result)

            product = Product(**AppConfig.db["products"].find_one({"id": product_id}))
            if not product:
                return json.dumps({"message": f"Product with ID {product_id} not found.", "success": False})

            success_response = {
                "message": f"Added {quantity} x {product.name} to your cart.",
                "success": True,
                "product": {"id": product.id, "name": product.name, "price": product.price},
                "quantity": quantity,
            }
            logger.info(f"Returning success response: {success_response}")
            return json.dumps(success_response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in add_to_cart_tool: {str(e)}")
            logger.error(f"Input that caused error: {repr(input_json)}")
            return json.dumps({"message": "Invalid JSON format in request.", "success": False})
        except Exception as e:
            logger.error(f"Error in add_to_cart_tool: {str(e)}")
            return json.dumps({"message": "Error occurred while adding to cart.", "success": False})

    def _extract_product_names_from_text(self, text: str) -> list:
        """Extract product names from the message text by matching against all product names in the database."""
        product_names = []
        all_products = [Product(**doc) for doc in AppConfig.db["products"].find()]
        for product in all_products:
            if product.name in text:
                product_names.append(product.name)
        return product_names

    def process_message(
        self, session_id: str, user_message: str, user_id: str = None
    ) -> Dict[str, Any]:
        """Process user message and generate AI response"""
        if not self.initialized:
            self.initialize()

        try:
            chat_session_data = AppConfig.db["chat_sessions"].find_one({"id": session_id})
            if not chat_session_data:
                chat_session = ChatSession(id=session_id, user_id=user_id)
                AppConfig.db["chat_sessions"].insert_one(chat_session.dict())
            else:
                chat_session = ChatSession(**chat_session_data)

            user_msg = Message(
                id=str(uuid.uuid4()),
                chat_session_id=session_id,
                content=user_message,
                is_bot=False,
                created_at=datetime.utcnow(),
            )
            # Convert products to JSON string as per Message model
            user_msg_dict = user_msg.dict()
            user_msg_dict["products"] = json.dumps(user_msg_dict.get("products", []))
            AppConfig.db["messages"].insert_one(user_msg_dict)

            memory = self.get_or_create_memory(session_id)
            chat_history = []
            if hasattr(memory, "buffer"):
                for msg in memory.buffer:
                    if hasattr(msg, "content"):
                        chat_history.append(msg.content)
                    elif isinstance(msg, str):
                        chat_history.append(msg)

            tools = self.create_tools()
            agent = initialize_agent(
                tools=tools,
                llm=self.llm,
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                memory=memory,
                verbose=True,
                handle_parsing_errors=True,
            )

            system_prompt = """You are Storey, an AI shopping assistant for an electronics e-commerce store.
            You help customers find the perfect tech products based on their needs and preferences.   

            Guidelines:            
            - Be helpful, friendly, and knowledgeable about technology products
            - Use the available tools to search for products, get details, and make recommendations
            - Always provide specific product suggestions when possible
            - Include prices, ratings, and key features in your responses
            - Ask clarifying questions if the user's request is unclear
            - Focus on electronics categories: smartphones, laptops, headphones, gaming equipment, smart home devices
            - When a user wants to add a product to cart, use the add_to_cart tool with the product name or ID
            - If the user says "add this to cart" or similar, use the product name from your recent message

            Available tools:
            - search_products: Find products using semantic search. Input: search query (str).
            - filter_products: Filter products. Input: JSON string with keys: category, subcategory, brand, min_price, max_price, min_rating, in_stock_only, features (list), search_query, limit.
            - get_product_details: Get product details. Input: product ID (str).
            - get_recommendations: Get recommendations. Input: product ID (str) or preference description (str).
            - add_to_cart: Add a product to the user's cart. Input: JSON string with keys: product_id (str or product name), quantity (int, optional, default 1).
            """

            agent_input = {"input": f"{system_prompt}\n\nUser: {user_message}"}
            result = agent(agent_input)
            ai_response = result["output"] if isinstance(result, dict) and "output" in result else str(result)

            product_ids = []
            if isinstance(result, dict) and "intermediate_steps" in result:
                for step in result["intermediate_steps"]:
                    tool_name = getattr(step[0], "tool", None) if hasattr(step[0], "tool") else None
                    tool_output = step[1]
                    if tool_name in ["search_products", "filter_products"]:
                        try:
                            parsed = json.loads(tool_output)
                            ids = parsed.get("product_ids", [])
                            if ids:
                                product_ids.extend(ids)
                        except Exception:
                            pass
            product_ids = list(dict.fromkeys(product_ids))

            message_text = ai_response
            if not product_ids:
                try:
                    parsed = json.loads(ai_response)
                    message_text = parsed.get("message", ai_response)
                    product_ids = parsed.get("product_ids", [])
                except Exception:
                    pass

            if not product_ids:
                product_names = self._extract_product_names_from_text(message_text)
                if product_names:
                    product_ids = [p.id for p in [Product(**doc) for doc in AppConfig.db["products"].find({"name": {"$in": product_names}})]]

            ai_msg = Message(
                id=str(uuid.uuid4()),
                chat_session_id=session_id,
                content=message_text,
                is_bot=True,
                message_type="product" if product_ids else "text",
                created_at=datetime.utcnow(),
            )
            # Convert products to JSON string
            ai_msg_dict = ai_msg.dict()
            ai_msg_dict["products"] = json.dumps(product_ids if product_ids else [])
            AppConfig.db["messages"].insert_one(ai_msg_dict)

            products = []
            if product_ids:
                products = [Product(**AppConfig.db["products"].find_one({"id": pid})).to_dict() for pid in product_ids if AppConfig.db["products"].find_one({"id": pid})]

            return {
                "id": ai_msg.id,
                "content": message_text,
                "isBot": True,
                "timestamp": ai_msg.created_at.isoformat() if ai_msg.created_at else datetime.utcnow().isoformat(),
                "products": products,
                "type": ai_msg.message_type,
            }

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            error_msg = Message(
                id=str(uuid.uuid4()),
                chat_session_id=session_id,
                content="I'm sorry, I encountered an error. Please try again.",
                is_bot=True,
                created_at=datetime.utcnow(),
            )
            error_msg_dict = error_msg.dict()
            error_msg_dict["products"] = json.dumps([])
            AppConfig.db["messages"].insert_one(error_msg_dict)
            return {
                "id": error_msg.id,
                "content": error_msg.content,
                "isBot": True,
                "timestamp": error_msg.created_at.isoformat() if error_msg.created_at else datetime.utcnow().isoformat(),
                "products": [],
                "type": "text",
            }

    def _extract_product_ids_from_response(self, response: str) -> List[str]:
        """Extract product IDs from AI response (basic implementation)"""
        product_ids = []
        return product_ids

    def get_chat_history(
        self, session_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get chat history for a session"""
        try:
            messages = [
                Message(**{k: v for k, v in doc.items() if k in Message.__fields__})  # Filter only valid fields
                for doc in AppConfig.db["messages"].find({"chat_session_id": session_id}).sort("created_at", 1).limit(limit)
            ]
            return [msg.to_dict(include_product_details=True) for msg in messages]
        except Exception as e:
            logger.error(f"Error getting chat history: {str(e)}")
            return []

    def clear_session_memory(self, session_id: str):
        """Clear memory for a specific session"""
        if session_id in self.memory_sessions:
            del self.memory_sessions[session_id]