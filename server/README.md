# E-commerce Chatbot Backend API

A comprehensive Flask-based REST API for an intelligent e-commerce chatbot with vector search capabilities, LangChain integration, and Google Gemini AI.

## Features

### 🤖 Intelligent Chatbot
- **LangChain Integration**: Advanced conversation management with memory
- **Google Gemini Flash 2.0**: State-of-the-art language model with 1M token context
- **Tool Calling**: Dynamic product search, filtering, and recommendations
- **Session Management**: Persistent conversation history and context

### 🔍 Advanced Search
- **Pinecone Vector Database**: Semantic product search and similarity matching
- **Embedding Generation**: Automatic product vectorization using Sentence Transformers
- **Hybrid Search**: Combines vector similarity with traditional filtering
- **Real-time Recommendations**: Context-aware product suggestions

### 🛍️ Product Management
- **Comprehensive Product Catalog**: 100+ electronics products across multiple categories
- **Advanced Filtering**: Price range, brand, category, rating, stock status
- **Dynamic Pricing**: Sale prices, discounts, and promotional offers
- **Inventory Management**: Real-time stock tracking

### 🔐 Authentication & Security
- **JWT Authentication**: Secure token-based authentication
- **User Management**: Registration, login, preferences, session management
- **Role-based Access**: Admin endpoints for product management
- **CORS Configuration**: Secure cross-origin resource sharing

## Technology Stack

### Core Framework
- **Flask**: Lightweight and flexible web framework
- **SQLAlchemy**: Powerful ORM for database operations
- **Flask-Migrate**: Database migration management
- **Flask-JWT-Extended**: JWT token management

### AI & Machine Learning
- **LangChain**: LLM orchestration and chain management
- **Google Gemini Flash 2.0**: Advanced language model
- **Pinecone**: Cloud-based vector database
- **Sentence Transformers**: Text embedding generation

### Database & Storage
- **SQLite**: Development database (easily replaceable)
- **Pinecone**: Vector storage for semantic search
- **Flask-SQLAlchemy**: Database abstraction layer

## Installation & Setup

### Prerequisites
- Python 3.8+
- Pinecone account and API key
- Google AI Studio API key

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
GOOGLE_API_KEY=your-google-api-key-here
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### 3. Database Initialization
```bash
# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed with sample data (automatic on first run)
python app.py
```

### 4. Run the Application
```bash
# Development mode
python app.py

# Or using Flask CLI
flask run

# Production mode
python run.py
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info
- `PUT /api/auth/preferences` - Update user preferences

### Products
- `GET /api/products/` - Get products with filtering
- `GET /api/products/<id>` - Get specific product
- `POST /api/products/search` - Advanced semantic search
- `GET /api/products/recommendations` - Get recommendations
- `GET /api/products/categories` - Get all categories
- `GET /api/products/brands` - Get all brands
- `GET /api/products/stats` - Get product statistics

### Chat
- `POST /api/chat/message` - Send message to chatbot
- `GET /api/chat/history/<session_id>` - Get chat history
- `GET /api/chat/sessions` - Get user's chat sessions
- `DELETE /api/chat/sessions/<id>` - Delete chat session
- `POST /api/chat/sessions/<id>/clear` - Clear chat history
- `GET /api/chat/health` - Check chat service health

### System
- `GET /api/health` - API health check

## Configuration

### Environment Variables
```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///ecommerce.db

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Google Gemini API
GOOGLE_API_KEY=your-google-api-key-here

# Pinecone Configuration
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment
PINECONE_INDEX_NAME=ecommerce-products

# CORS Configuration
FRONTEND_URL=http://localhost:5173
```

### Database Models

#### User
- User authentication and preferences
- JWT token management
- Chat session relationships

#### Product
- Comprehensive product information
- Vector embedding integration
- Advanced search capabilities

#### ChatSession
- Conversation management
- User association
- Session metadata

#### Message
- Individual chat messages
- Product associations
- Message types and metadata

## Services Architecture

### VectorService
- Pinecone integration
- Embedding generation
- Similarity search
- Batch operations

### ChatService
- LangChain orchestration
- Gemini AI integration
- Tool calling
- Memory management

### ProductService
- Product CRUD operations
- Search and filtering
- Recommendation engine
- Embedding management

### AuthService
- User authentication
- JWT token management
- Preference handling
- Security validation

## Development

### Adding New Products
```python
from services.product_service import ProductService

product_service = ProductService()
product_data = {
    'name': 'New Product',
    'description': 'Product description',
    'price': 299.99,
    'category': 'Electronics',
    'subcategory': 'Smartphones',
    'brand': 'Brand Name',
    'features': ['Feature 1', 'Feature 2']
}

product = product_service.create_product(product_data)
```

### Custom Chat Tools
```python
from langchain.tools import Tool

def custom_tool_function(input_text):
    # Your custom logic here
    return "Tool response"

custom_tool = Tool(
    name="custom_tool",
    description="Description of what the tool does",
    func=custom_tool_function
)
```

### Vector Search
```python
from services.vector_service import VectorService

vector_service = VectorService()
vector_service.initialize()

# Search for similar products
results = vector_service.search_similar_products(
    "gaming laptop with RTX graphics",
    top_k=10
)
```

## Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use strong secret keys
- [ ] Configure production database
- [ ] Set up proper logging
- [ ] Configure CORS for production domain
- [ ] Use HTTPS
- [ ] Set up monitoring

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run.py"]
```

### Environment-specific Configurations
- Development: SQLite, debug mode, verbose logging
- Production: PostgreSQL/MySQL, optimized settings, error logging

## Monitoring & Logging

### Log Files
- `logs/ecommerce_chatbot.log` - Application logs
- Rotating file handler (10MB max, 10 backups)
- Console and file output

### Health Checks
- `/api/health` - Basic API health
- `/api/chat/health` - Chat service health
- Vector database statistics
- Service initialization status

## Troubleshooting

### Common Issues

1. **Pinecone Connection Error**
   - Verify API key and environment
   - Check network connectivity
   - Ensure index exists

2. **Google AI API Error**
   - Verify API key
   - Check quota limits
   - Ensure proper model access

3. **Database Migration Issues**
   - Delete migration files and reinitialize
   - Check database permissions
   - Verify SQLAlchemy models

4. **Memory Issues**
   - Monitor conversation memory usage
   - Clear old sessions periodically
   - Optimize embedding storage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.