# OpenShift Partner Labs Agents

AI-powered form-filling agent for OpenShift lab requests using AgentOS with Agno framework and Agno UI.

## 🏗️ Architecture

This project implements an AI-powered conversational agent that guides users through filling out OpenShift lab request forms. The system uses:

- **Backend**: AgentOS with Agno framework for AI agent capabilities
- **Frontend**: Agno UI (AG-UI) for the native chat interface
- **Database**: MySQL for data persistence
- **AI**: OpenAI models via Agno framework

## 📁 Project Structure

```
openshift-partner-labs-agents/
├── backend/                 # AgentOS backend with Agno agent
│   ├── app/                # Main application package
│   │   ├── __init__.py
│   │   ├── main.py         # AgentOS application
│   │   ├── core/           # Core application components
│   │   │   ├── __init__.py
│   │   │   ├── config.py   # Configuration settings
│   │   │   └── database.py # Database connection
│   │   ├── models/         # Database models
│   │   │   ├── __init__.py
│   │   │   ├── base.py     # Base model class
│   │   │   └── request.py  # Request model
│   │   ├── services/       # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── session_manager.py # Session state management
│   │   │   └── validation.py      # Data validation utilities
│   │   └── agents/         # AI agents
│   │       ├── __init__.py
│   │       ├── form_agent.py # Main form-filling agent
│   │       ├── tools.py      # Agent tool belt
│   │       └── prompts.py    # AI agent prompts
│   ├── run.py              # Server runner script
│   ├── requirements.txt    # Backend dependencies
│   └── alembic.ini         # Database migration config
├── .env.example            # Environment configuration template
├── DEVELOPMENT-GUIDE.md    # Detailed development guide
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (recommended: Python 3.9+)
- **MySQL database** (version 8.0+)
- **Agno API key** (get from [Agno platform](https://agno.ai))
- **Node.js 18+** (for Agno UI frontend)
- **pnpm** (package manager for Node.js)

**For Development (Ollama):**
- **Ollama** installed locally
- At least **8GB RAM** for local models
- **Docker** (optional, for Ollama container)

**For Production (OpenAI):**
- **OpenAI API key** (get from [OpenAI platform](https://platform.openai.com))

### Step-by-Step Installation

#### 1. Clone and Setup Repository

```bash
# Clone the repository
git clone <repository-url>
cd openshift-partner-labs-agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r backend/requirements.txt
```

#### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit the .env file with your configuration
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
```bash
# Required Configuration
AGNO_API_KEY=your_agno_api_key_here
DATABASE_URL=mysql+mysqlconnector://username:password@localhost:3306/openshift_labs

# Model Configuration (choose one)
MODEL_TYPE=ollama  # for development
# MODEL_TYPE=openai  # for production

# Ollama Configuration (for development)
OLLAMA_MODEL=llama3.2:latest
OLLAMA_HOST=http://localhost:11434

# OpenAI Configuration (for production)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Session Configuration
SESSION_SECRET_KEY=your-secret-key-here
SESSION_EXPIRE_HOURS=24
```

#### 3. Database Setup

```bash
# Install MySQL (if not already installed)
# On macOS with Homebrew:
brew install mysql
brew services start mysql

# On Ubuntu/Debian:
sudo apt update
sudo apt install mysql-server

# Create database and user
mysql -u root -p
```

In MySQL console:
```sql
CREATE DATABASE openshift_labs;
CREATE USER 'openshift_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON openshift_labs.* TO 'openshift_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Update your `.env` file with the database credentials:
```bash
DATABASE_URL=mysql+mysqlconnector://openshift_user:your_password@localhost:3306/openshift_labs
```

#### 4. Initialize Database Tables

```bash
cd backend
python -c "from app.core.database import create_tables; create_tables()"
```

#### 5. AI Model Setup

**Option A: Development with Ollama (Recommended for local development)**

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# In another terminal, pull the model
ollama pull llama3.2:latest

# Run the Ollama setup script
python setup_ollama.py
```

**Option B: Production with OpenAI**

```bash
# Set your OpenAI API key in .env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_TYPE=openai
```

#### 6. Agno UI Frontend Setup

```bash
# Install pnpm if not already installed
npm install -g pnpm

# Clone the Agno UI repository
git clone https://github.com/ag-ui-protocol/ag-ui.git
cd ag-ui

# Install dependencies
cd typescript-sdk
pnpm install

# Build the Agno package
cd ../integrations/agno
pnpm run build

# Return to project root
cd ../../..
```

### Running the Application

#### 1. Start the Backend Server

```bash
# From project root
cd backend
python run.py
```

The AgentOS backend will be available at `http://localhost:8000`

#### 2. Start the Agno UI Frontend

```bash
# In a new terminal, from the ag-ui directory
cd ag-ui

# Start Dojo (Agno UI frontend)
# Follow the specific instructions in the ag-ui repository
# Typically involves running a development server
```

The UI will typically be available at `http://localhost:3000`

#### 3. Verify Installation

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Database Connection:**
   ```bash
   cd backend
   python -c "from app.core.database import test_connection; test_connection()"
   ```

3. **AI Model Test:**
   ```bash
   # For Ollama
   curl http://localhost:11434/api/generate -d '{"model": "llama3.2:latest", "prompt": "Hello"}'
   
   # For OpenAI (test with your API key)
   curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
   ```

## 🔧 Configuration

### Model Configuration

The application supports two model backends:

**For Development (Ollama):**
- Free and runs locally
- No API keys required
- Good for development and testing
- Requires local installation

**For Production (OpenAI):**
- Cloud-based with API keys
- More powerful models
- Requires OpenAI API key
- Better for production use

### Environment Variables

Copy `.env.example` to `.env` and update the following variables:

```bash
# Required Configuration
AGNO_API_KEY=your_agno_api_key_here
DATABASE_URL=mysql+mysqlconnector://username:password@localhost:3306/openshift_labs

# Model Configuration
MODEL_TYPE=ollama  # or "openai" for production

# Ollama Configuration (for development)
OLLAMA_MODEL=llama3.2:latest
OLLAMA_HOST=http://localhost:11434

# OpenAI Configuration (for production)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Session Configuration
SESSION_SECRET_KEY=your-secret-key-here
SESSION_EXPIRE_HOURS=24

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0
```

### Database Configuration

The application uses MySQL for data persistence. The database schema includes:

- **requests** table: Stores all lab request information
- **Auto-generated fields**: timestamps, request state, evaluation dates
- **User fields**: company info, contact details, project specifications
- **Technical fields**: OpenShift version, cluster requirements, cloud provider

See `backend/app/models/request.py` for the complete schema.

## 🛠️ Development

### Development Setup

1. **Install Development Dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   pip install pytest black flake8
   ```

2. **Run Tests:**
   ```bash
   cd backend
   pytest
   ```

3. **Code Formatting:**
   ```bash
   black backend/
   flake8 backend/
   ```

4. **Database Migrations:**
   ```bash
   cd backend
   alembic upgrade head
   ```

### Troubleshooting

**Common Issues:**

1. **Database Connection Error:**
   ```bash
   # Check MySQL service
   brew services list | grep mysql  # macOS
   sudo systemctl status mysql     # Linux
   
   # Test connection
   mysql -u openshift_user -p openshift_labs
   ```

2. **Ollama Not Responding:**
   ```bash
   # Check Ollama service
   curl http://localhost:11434/api/tags
   
   # Restart Ollama
   ollama serve
   ```

3. **Agno UI Build Issues:**
   ```bash
   # Clear node modules and reinstall
   cd ag-ui
   rm -rf node_modules
   pnpm install
   ```

4. **Python Import Errors:**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```

### Logs and Debugging

**Backend Logs:**
```bash
cd backend
python run.py --log-level debug
```

**Database Logs:**
```bash
# MySQL logs
tail -f /var/log/mysql/error.log  # Linux
tail -f /usr/local/var/mysql/*.err  # macOS
```

**Ollama Logs:**
```bash
# Check Ollama logs
ollama logs
```

## 🤖 AI Agent Features

The Agno-powered agent provides:

- **Conversational Interface**: Natural language interaction
- **Form Validation**: Real-time data validation
- **Session Management**: Persistent conversation state
- **Tool Integration**: Database operations and data processing
- **Smart Prompts**: Context-aware responses

### Available Tools

- `get_session_data`: Retrieve current form data
- `update_form_data`: Save user input to session
- `validate_data`: Validate field values
- `check_form_completeness`: Verify all required fields
- `submit_form`: Submit completed form to database
- `get_form_summary`: Get form summary for confirmation

### Form Fields

The agent collects the following information:

**Required Fields:**
- Company information (name, contacts, sponsor)
- Project details (name, start date, duration, timezone)
- Technical specifications (OpenShift version, cluster size, cloud provider)
- Application details (type, request type, description, scope of work)

**Conditional Fields:**
- Cluster requirements (only if virtualization is enabled)

**Optional Fields:**
- Secondary contact information
- Additional notes

## 🎨 Agno UI Interface

The application uses Agno UI (AG-UI) for the frontend interface, which provides:

- **Native Agno Integration**: Built specifically for Agno agents
- **ChatGPT-like Experience**: Familiar chat interface
- **Real-time Chat**: Instant message exchange
- **Markdown Support**: Rich text formatting in responses
- **DateTime Context**: Time-aware responses
- **Open Protocol**: Compatible with AG-UI frontends

### AgentOS Endpoints

AgentOS automatically provides all necessary endpoints for:
- Agent communication
- Session management
- Memory management
- Knowledge management
- Metrics collection

The AG-UI interface handles all user interactions through the native Agno protocol.

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
# Start Agno UI (Dojo)
cd ag-ui
# Follow the Dojo startup instructions
# Test the interface manually
```

### Manual Testing

1. Start the AgentOS backend
2. Start the Agno UI frontend
3. Open the Agno UI interface
4. Select your OpenShift Lab Request Agent
5. Start a conversation
6. Follow the form-filling flow
7. Verify form submission

## 🚀 Deployment

### Production Considerations

1. **Database**: Use a production MySQL instance
2. **Session Storage**: Replace in-memory sessions with Redis
3. **Authentication**: Implement proper JWT token validation
4. **Security**: Add rate limiting and input sanitization
5. **Monitoring**: Add logging and metrics collection

### Docker Deployment

Create `Dockerfile` for each service:

```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

### Environment Setup

For production deployment:

1. Set up MySQL database
2. Configure Redis for session storage
3. Set up proper authentication
4. Configure logging and monitoring
5. Set up SSL/TLS certificates
6. Configure load balancing

## 📚 Development Guide

For detailed development information, see `Development-guide.md`.

## 🚀 Deployment

### Production Considerations

1. **Database**: Use a production MySQL instance
2. **Session Storage**: Replace in-memory sessions with Redis
3. **Authentication**: Implement proper JWT token validation
4. **Security**: Add rate limiting and input sanitization
5. **Monitoring**: Add logging and metrics collection

### Docker Deployment

Create `Dockerfile` for each service:

```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

### Environment Setup

For production deployment:

1. Set up MySQL database
2. Configure Redis for session storage
3. Set up proper authentication
4. Configure logging and monitoring
5. Set up SSL/TLS certificates
6. Configure load balancing

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
# Start Agno UI (Dojo)
cd ag-ui
# Follow the Dojo startup instructions
# Test the interface manually
```

### Manual Testing

1. Start the AgentOS backend
2. Start the Agno UI frontend
3. Open the Agno UI interface
4. Select your OpenShift Lab Request Agent
5. Start a conversation
6. Follow the form-filling flow
7. Verify form submission

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the development guide
- Review the API documentation
- Open an issue on GitHub