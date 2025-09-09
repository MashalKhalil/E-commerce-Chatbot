# E-Commerce Chatbot

A full-stack intelligent e-commerce chatbot application built with Next.js frontend and Flask backend. The chatbot uses Google Gemini AI and Pinecone vector database to provide intelligent product recommendations and customer support.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Backend Setup (Flask)](#backend-setup-flask)
  - [Frontend Setup (Next.js)](#frontend-setup-nextjs)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The application consists of two main components:

1. **Backend (Flask API)** - Located in `/server/`
   - RESTful API with Flask
   - SQLAlchemy for database management
   - JWT authentication
   - Google Gemini AI integration
   - Pinecone vector database for product search
   - SQLite/PostgreSQL database support

2. **Frontend (Next.js)** - Located in `/apps/web/`
   - Modern React-based UI with Next.js 15
   - TypeScript support
   - Tailwind CSS for styling
   - Radix UI components
   - Real-time chat interface

## Features

- 🤖 AI-powered chatbot with Google Gemini
- 🔍 Intelligent product search using vector embeddings
- 🛒 Shopping cart management
- 👤 User authentication and profiles
- 📱 Responsive design
- 🔒 JWT-based security
- 📊 Real-time chat sessions
- 🎨 Modern UI with dark/light mode support

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (for backend)
- **Node.js 18+** (for frontend)
- **npm or yarn** (for package management)
- **Git** (for version control)

### Required API Keys

You'll need to obtain the following API keys:

1. **Google Gemini API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key

2. **Pinecone API Key** (required for vector search and AI recommendations)
   - Visit [Pinecone](https://www.pinecone.io/)
   - Create an account and get API credentials

## Installation

### Clone the Repository

```bash
git clone <your-repository-url>
cd website-bot/ecommerce-chatbot
```

### Backend Setup (Flask)

1. **Navigate to the server directory:**
   ```bash
   cd server
   ```

2. **Create a Python virtual environment:**
   ```bash
   # Using venv
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   ```

5. **Edit the `.env` file with your configuration:**
   ```bash
   # Required configurations
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-super-secret-key-here
   
   # Database (SQLite for development)
   DATABASE_URL=sqlite:///ecommerce.db
   
   # JWT Configuration
   JWT_SECRET_KEY=your-jwt-secret-key-here
   JWT_ACCESS_TOKEN_EXPIRES=3600
   
   # Google Gemini API (Required)
   GOOGLE_API_KEY=your-google-api-key-here
   
   # Pinecone Configuration (Required for vector search)
   PINECONE_API_KEY=your-pinecone-api-key-here
   PINECONE_ENVIRONMENT=your-pinecone-environment
   PINECONE_INDEX_NAME=ecommerce-products
   
   # Frontend URL
   FRONTEND_URL=http://localhost:3000
   ```

### Frontend Setup (Next.js)

1. **Navigate to the web app directory:**
   ```bash
   cd ../apps/web
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment variables (if needed):**
   ```bash
   # Create .env.local file
   echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > .env.local
   ```

## Environment Configuration

### Backend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FLASK_APP` | Yes | `app.py` | Flask application entry point |
| `FLASK_ENV` | No | `development` | Flask environment mode |
| `SECRET_KEY` | Yes | - | Flask secret key for sessions |
| `DATABASE_URL` | No | `sqlite:///ecommerce.db` | Database connection string |
| `JWT_SECRET_KEY` | Yes | - | JWT token secret key |
| `JWT_ACCESS_TOKEN_EXPIRES` | No | `3600` | JWT token expiration time (seconds) |
| `GOOGLE_API_KEY` | Yes | - | Google Gemini API key |
| `PINECONE_API_KEY` | Yes | - | Pinecone vector database API key |
| `PINECONE_ENVIRONMENT` | Yes | - | Pinecone environment |
| `PINECONE_INDEX_NAME` | No | `ecommerce-products` | Pinecone index name |
| `FRONTEND_URL` | No | `http://localhost:5173` | Frontend URL for CORS |

### Frontend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | No | `http://localhost:5000` | Backend API URL |

## Pinecone Vector Database Setup

This application requires Pinecone for vector-based product search and AI recommendations. Here are the detailed configuration requirements:

### Pinecone Index Configuration

You need to create a Pinecone index with the following specifications:

| Setting | Value | Description |
|---------|-------|-------------|
| **Index Name** | `ecommerce-products` | Name of your Pinecone index |
| **Dimensions** | `384` | Vector dimension for embeddings |
| **Metric** | `cosine` | Distance metric for similarity search |
| **Cloud Provider** | `AWS` or `GCP` | Your preferred cloud provider |
| **Region** | `us-east-1` (AWS) or `us-central1-gcp` (GCP) | Closest region to your deployment |

### Creating Your Pinecone Index

1. **Sign up at [Pinecone](https://www.pinecone.io/)**
2. **Create a new index with these settings:**
   ```bash
   # Via Pinecone Console (Recommended)
   - Index name: ecommerce-products
   - Dimensions: 384
   - Metric: cosine
   - Cloud: AWS or GCP
   - Region: us-east-1 (or your preferred region)
   ```

3. **Get your API credentials:**
   - API Key: Found in your Pinecone console
   - Environment: Your Pinecone environment (e.g., `us-east-1-aws`)

### Embedding Model Configuration

The application uses the following embedding model:

| Setting | Value | Description |
|---------|-------|-------------|
| **Model** | `all-MiniLM-L6-v2` | Sentence Transformer model |
| **Dimensions** | `384` | Output vector dimensions |
| **Max Sequence Length** | `256 tokens` | Maximum input text length |
| **Model Size** | `~80MB` | Approximate model size |

### Important Notes

- **Dimension Matching**: The Pinecone index dimensions (384) must exactly match the embedding model output dimensions
- **Metric Choice**: Cosine similarity is optimal for sentence transformer embeddings
- **Environment**: Make sure your `PINECONE_ENVIRONMENT` matches your actual Pinecone environment
- **Regional Performance**: Choose a Pinecone region closest to your application deployment for best performance

### Verifying Your Setup

After configuration, you can verify your Pinecone setup by running:

```bash
cd server
python -c "from services.vector_service import VectorService; vs = VectorService(); vs.initialize(); print('Pinecone setup successful!')"
```

## Database Setup

The application uses SQLAlchemy with Flask-Migrate for database management.

### Initialize Database

```bash
cd server

# Initialize migration repository (first time only)
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Database Seeding

The application automatically seeds the database with sample products when you first run it. This happens through the `initialize_database()` function in `app.py`.

### Using PostgreSQL (Production)

For production, you can use PostgreSQL:

1. **Install PostgreSQL dependencies:**
   ```bash
   pip install psycopg2-binary
   ```

2. **Update DATABASE_URL in .env:**
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_db
   ```

## Running the Application

### Development Mode

You'll need to run both the backend and frontend in separate terminal sessions:

#### Terminal 1: Start Backend Server

```bash
cd server

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Run Flask development server
python app.py
# or
flask run

# Server will start at http://localhost:5000
```

#### Terminal 2: Start Frontend Server

```bash
cd apps/web

# Start Next.js development server
npm run dev
# or
yarn dev

# Frontend will start at http://localhost:3000
```

### Production Mode

#### Backend (using Gunicorn)

```bash
cd server

# Install Gunicorn (if not already installed)
pip install gunicorn

# Run with Gunicorn
gunicorn -c gunicorn.conf.py app:app

# Or manually
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

#### Frontend (Next.js Build)

```bash
cd apps/web

# Build for production
npm run build

# Start production server
npm run start
```

## API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Product Endpoints

- `GET /api/products` - Get all products
- `GET /api/products/{id}` - Get specific product
- `GET /api/products/search?q={query}` - Search products

### Cart Endpoints

- `GET /api/cart` - Get user's cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update` - Update cart item
- `DELETE /api/cart/remove/{item_id}` - Remove item from cart
- `POST /api/cart/clear` - Clear entire cart

### Chat Endpoints

- `POST /api/chat/message` - Send message to chatbot
- `GET /api/chat/sessions` - Get chat sessions
- `GET /api/chat/sessions/{session_id}` - Get specific session
- `POST /api/chat/sessions` - Create new chat session

### Health Check

- `GET /api/health` - API health status

## Project Structure

```
ecommerce-chatbot/
├── server/                          # Flask Backend
│   ├── models/                      # Database models
│   │   ├── __init__.py
│   │   ├── user.py                 # User model
│   │   ├── product.py              # Product model
│   │   ├── cart.py                 # Cart model
│   │   ├── chat_session.py         # Chat session model
│   │   └── message.py              # Message model
│   ├── routes/                      # API routes
│   │   ├── __init__.py
│   │   ├── auth.py                 # Authentication routes
│   │   ├── products.py             # Product routes
│   │   ├── cart.py                 # Cart routes
│   │   └── chat.py                 # Chat routes
│   ├── services/                    # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py         # Authentication service
│   │   ├── product_service.py      # Product service
│   │   ├── cart_service.py         # Cart service
│   │   └── chat_service.py         # Chat/AI service
│   ├── utils/                       # Utilities
│   │   ├── __init__.py
│   │   ├── logger_config.py        # Logging configuration
│   │   ├── database_seeder.py      # Database seeding
│   │   └── decorators.py           # Custom decorators
│   ├── migrations/                  # Database migrations
│   ├── app.py                      # Flask application factory
│   ├── config.py                   # Configuration settings
│   ├── requirements.txt            # Python dependencies
│   ├── gunicorn.conf.py           # Gunicorn configuration
│   ├── .env.example               # Environment variables template
│   └── run.py                     # Development server runner
├── apps/web/                       # Next.js Frontend
│   ├── app/                        # App router pages
│   │   ├── layout.tsx             # Root layout
│   │   ├── page.tsx               # Home page
│   │   ├── chat/                  # Chat pages
│   │   ├── products/              # Product pages
│   │   ├── cart/                  # Cart page
│   │   ├── login/                 # Login page
│   │   ├── register/              # Register page
│   │   └── profile/               # Profile pages
│   ├── components/                 # Reusable components
│   │   ├── ui/                    # Base UI components
│   │   ├── layout/                # Layout components
│   │   ├── chat/                  # Chat-specific components
│   │   └── products/              # Product-specific components
│   ├── context/                    # React contexts
│   ├── lib/                       # Utility functions
│   ├── public/                    # Static assets
│   ├── package.json               # Node.js dependencies
│   ├── next.config.js             # Next.js configuration
│   ├── tailwind.config.js         # Tailwind CSS configuration
│   ├── tsconfig.json              # TypeScript configuration
│   └── components.json            # shadcn/ui configuration
└── README.md                      # This file
```

## Development

### Adding New Features

1. **Backend**: Add new routes in `routes/`, implement business logic in `services/`, and create/update models in `models/`
2. **Frontend**: Create new pages in `app/`, add components in `components/`, and update types as needed

### Code Style

- **Backend**: Follow PEP 8 Python style guidelines
- **Frontend**: Use ESLint and Prettier for code formatting
- **Database**: Use descriptive model names and follow SQLAlchemy best practices

### Running Tests

```bash
# Backend tests (if implemented)
cd server
python -m pytest

# Frontend tests (if implemented)
cd apps/web
npm run test
```

### Linting

```bash
# Frontend linting
cd apps/web
npm run lint
```

## Production Deployment

### Environment Setup

1. Set `FLASK_ENV=production` in your environment
2. Use a proper database (PostgreSQL recommended)
3. Set strong secret keys for `SECRET_KEY` and `JWT_SECRET_KEY`
4. Configure proper CORS settings
5. Use environment-specific configurations

### Deployment Options

#### Using Docker (Recommended)

Create `Dockerfile` for each service and use `docker-compose` for orchestration.

#### Traditional Server Deployment

1. **Backend**: Deploy Flask app using Gunicorn + Nginx
2. **Frontend**: Build Next.js app and serve with Nginx or deploy to Vercel/Netlify
3. **Database**: Use managed PostgreSQL service (AWS RDS, Google Cloud SQL, etc.)

#### Cloud Platforms

- **Heroku**: Easy deployment for both frontend and backend
- **Vercel**: Excellent for Next.js frontend
- **AWS**: Full-featured deployment with EC2, RDS, S3
- **Google Cloud Platform**: Comprehensive cloud solution
- **DigitalOcean**: Simple and cost-effective VPS deployment

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors

```bash
# Check if database file exists and has proper permissions
ls -la server/ecommerce.db

# Reset database
rm server/ecommerce.db
cd server && flask db upgrade
```

#### 2. CORS Errors

Make sure `FRONTEND_URL` in your backend `.env` matches your frontend URL:
```bash
# If frontend runs on port 3000
FRONTEND_URL=http://localhost:3000
```

#### 3. API Key Issues

Verify your API keys are correctly set:
```bash
# Check if environment variables are loaded
cd server
python -c "import os; print('GOOGLE_API_KEY:', bool(os.getenv('GOOGLE_API_KEY')))"
```

#### 4. Port Already in Use

```bash
# Kill processes using ports 3000 or 5000
# On Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux
lsof -ti:5000 | xargs kill -9
```

#### 5. Node.js Module Issues

```bash
cd apps/web
rm -rf node_modules package-lock.json
npm install
```

#### 6. Python Package Issues

```bash
cd server
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Getting Help

- Check the [Flask documentation](https://flask.palletsprojects.com/)
- Review [Next.js documentation](https://nextjs.org/docs)
- Look at [Google Gemini API docs](https://ai.google.dev/docs)
- Check [Pinecone documentation](https://docs.pinecone.io/) for vector database issues

### Log Files

- **Backend logs**: Check Flask console output or configure logging to files
- **Frontend logs**: Check browser developer console and Next.js console output

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Happy coding! 🚀**

If you encounter any issues or have questions, please feel free to open an issue in the repository.#   e c o m m e r c e - c h a t b o t  
 