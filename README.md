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
- [Contributing](#contributing)
- [License](#license)

## Architecture Overview

The application consists of two main components:

1. **Backend (Flask API)**
   - Located in `/server/`
   - RESTful API with Flask
   - SQLAlchemy for database management
   - JWT authentication
   - Google Gemini AI integration
   - Pinecone vector database for product search
   - SQLite/PostgreSQL database support

2. **Frontend (Next.js)**
   - Located in `/apps/web/`
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
git clone <repository-url>
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

| Variable                   | Required | Default                  | Description                         |
| -------------------------- | -------- | ------------------------ | ----------------------------------- |
| `FLASK_APP`                | Yes      | `app.py`                 | Flask application entry point       |
| `FLASK_ENV`                | No       | `development`            | Flask environment mode              |
| `SECRET_KEY`               | Yes      | -                        | Flask secret key for sessions       |
| `DATABASE_URL`             | No       | `sqlite:///ecommerce.db` | Database connection string          |
| `JWT_SECRET_KEY`           | Yes      | -                        | JWT token secret key                |
| `JWT_ACCESS_TOKEN_EXPIRES` | No       | `3600`                   | JWT token expiration time (seconds) |
| `GOOGLE_API_KEY`           | Yes      | -                        | Google Gemini API key               |
| `PINECONE_API_KEY`         | Yes      | -                        | Pinecone vector database API key    |
| `PINECONE_ENVIRONMENT`     | Yes      | -                        | Pinecone environment                |
| `PINECONE_INDEX_NAME`      | No       | `ecommerce-products`     | Pinecone index name                 |
| `FRONTEND_URL`             | No       | `http://localhost:5173`  | Frontend URL for CORS               |

### Frontend Environment Variables

| Variable              | Required | Default                 | Description     |
| --------------------- | -------- | ----------------------- | --------------- |
| `NEXT_PUBLIC_API_URL` | No       | `http://localhost:5000` | Backend API URL |

## Pinecone Vector Database Setup

This application requires Pinecone for vector-based product search and AI recommendations.

### Pinecone Index Configuration

Create a Pinecone index with these specifications:

| Setting            | Value                                        | Description                           |
| ------------------ | -------------------------------------------- | ------------------------------------- |
| **Index Name**     | `ecommerce-products`                         | Name of your Pinecone index           |
| **Dimensions**     | `384`                                        | Vector dimension for embeddings       |
| **Metric**         | `cosine`                                     | Distance metric for similarity search |
| **Cloud Provider** | `AWS` or `GCP`                               | Your preferred cloud provider         |
| **Region**         | `us-east-1` (AWS) or `us-central1-gcp` (GCP) | Closest region to your deployment     |

### Creating Your Pinecone Index

1. **Sign up at [Pinecone](https://www.pinecone.io/)**
2. **Create a new index with these settings:**

```bash
# Via Pinecone Console
- Index name: ecommerce-products
- Dimensions: 384
- Metric: cosine
- Cloud: AWS or GCP
- Region: us-east-1 (or your preferred region)
```

3. **Get your API credentials**

   * API Key: Found in your Pinecone console
   * Environment: Your Pinecone environment (e.g., `us-east-1-aws`)

### Embedding Model Configuration

| Setting                 | Value              | Description                |
| ----------------------- | ------------------ | -------------------------- |
| **Model**               | `all-MiniLM-L6-v2` | Sentence Transformer model |
| **Dimensions**          | `384`              | Output vector dimensions   |
| **Max Sequence Length** | `256 tokens`       | Maximum input text length  |
| **Model Size**          | `~80MB`            | Approximate model size     |

### Important Notes

* **Dimension Matching**: Pinecone index dimensions must match embedding model output.
* **Metric Choice**: Cosine similarity is optimal for sentence transformer embeddings.
* **Environment**: Make sure `PINECONE_ENVIRONMENT` matches your Pinecone environment.
* **Regional Performance**: Choose the closest region for best performance.

### Verifying Your Setup

```bash
cd server
python -c "from services.vector_service import VectorService; vs = VectorService(); vs.initialize(); print('Pinecone setup successful!')"
```

## Database Setup

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

Database seeds automatically via `initialize_database()` in `app.py`.

### Using PostgreSQL (Production)

```bash
pip install psycopg2-binary
```

Update `.env`:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_db
```

## Running the Application

### Development Mode

Run backend and frontend in separate terminals:

#### Terminal 1: Backend

```bash
cd server
# Activate venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
python app.py
# or flask run
# http://localhost:5000
```

#### Terminal 2: Frontend

```bash
cd apps/web
npm run dev
# or yarn dev
# http://localhost:3000
```

### Production Mode

#### Backend (Gunicorn)

```bash
cd server
pip install gunicorn
gunicorn -c gunicorn.conf.py app:app
# or
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

#### Frontend (Next.js)

```bash
cd apps/web
npm run build
npm run start
```

## API Documentation

### Authentication Endpoints

* `POST /api/auth/register`
* `POST /api/auth/login`
* `POST /api/auth/refresh`
* `GET /api/auth/profile`
* `PUT /api/auth/profile`

### Product Endpoints

* `GET /api/products`
* `GET /api/products/{id}`
* `GET /api/products/search?q={query}`

### Cart Endpoints

* `GET /api/cart`
* `POST /api/cart/add`
* `PUT /api/cart/update`
* `DELETE /api/cart/remove/{item_id}`
* `POST /api/cart/clear`

### Chat Endpoints

* `POST /api/chat/message`
* `GET /api/chat/sessions`
* `GET /api/chat/sessions/{session_id}`
* `POST /api/chat/sessions`

### Health Check

* `GET /api/health`

## Project Structure

```
ecommerce-chatbot/
├── server/                 # Flask Backend
│   ├── models/             # Database models
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   ├── utils/              # Utilities
│   ├── migrations/         # Database migrations
│   ├── app.py              # Flask application
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   ├── gunicorn.conf.py    # Gunicorn config
│   └── .env.example        # Env template
├── apps/web/               # Next.js Frontend
│   ├── app/                # Pages
│   ├── components/         # Reusable components
│   ├── context/            # React contexts
│   ├── lib/                # Utilities
│   ├── public/             # Static assets
│   ├── package.json        # Node dependencies
│   ├── next.config.js      # Next.js config
│   └── tailwind.config.js  # Tailwind CSS config
└── README.md               # This file
```

## Development

### Adding New Features

* **Backend**: Add routes in `routes/`, logic in `services/`, update `models/`.
* **Frontend**: Add pages in `app/`, components in `components/`, update types.

### Code Style

* **Backend**: Follow PEP 8
* **Frontend**: Use ESLint and Prettier
* **Database**: Descriptive model names, SQLAlchemy best practices

### Running Tests

```bash
# Backend
cd server
python -m pytest

# Frontend
cd apps/web
npm run test
```

### Linting

```bash
cd apps/web
npm run lint
```

## Production Deployment

* Set `FLASK_ENV=production`
* Use PostgreSQL
* Strong secret keys
* Proper CORS settings

### Deployment Options

* **Docker**: Use `Dockerfile` for each service and `docker-compose`.
* **Traditional**: Flask + Gunicorn + Nginx, Next.js build served via Nginx or Vercel/Netlify.
* **Cloud Platforms**: Heroku, Vercel, AWS, GCP, DigitalOcean.

## Troubleshooting

### Database

```bash
ls -la server/ecommerce.db
rm server/ecommerce.db
cd server && flask db upgrade
```

### CORS

```bash
FRONTEND_URL=http://localhost:3000
```

### API Key Issues

```bash
cd server
python -c "import os; print('GOOGLE_API_KEY:', bool(os.getenv('GOOGLE_API_KEY')))"
```

### Ports

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Node.js Modules

```bash
cd apps/web
rm -rf node_modules package-lock.json
npm install
```

### Python Packages

```bash
cd server
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Getting Help

* [Flask Docs](https://flask.palletsprojects.com/)
* [Next.js Docs](https://nextjs.org/docs)
* [Google Gemini API](https://ai.google.dev/docs)
* [Pinecone Docs](https://docs.pinecone.io/)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

**Happy coding! 🚀**
