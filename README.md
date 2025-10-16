# OpenShift Partner Labs - Multi-Agent System

AI-powered multi-agent system for managing OpenShift Partner Labs operations using AgentOS with Agno framework and Agno UI.

## 🏗️ Architecture Overview

This project implements a multi-agent system where each agent handles specific tasks related to OpenShift Partner Labs. The system is built with:

- **Backend**: AgentOS with Agno framework for AI agent capabilities
- **Frontend**: Agno UI (AG-UI) for native chat interfaces
- **Database**: MySQL for data persistence
- **AI**: OpenAI/Ollama models via Agno framework

## 📁 Project Structure

```
openshift-partner-labs-agents/
├── README.md                          # This file - project overview
├── .env.example                       # Environment configuration template
├── backend/
│   ├── requirements.txt               # Shared Python dependencies
│   ├── run.py                         # Main server runner
│   ├── main.py                        # AgentOS application (registers all agents)
│   ├── alembic.ini                    # Database migration config
│   │
│   ├── common/                        # Shared utilities across all agents
│   │   ├── core/                      # Core functionality
│   │   │   ├── config.py              # Global configuration
│   │   │   └── database.py            # Database connection & utilities
│   │   └── services/                  # Shared services
│   │       └── session_manager.py     # Session state management
│   │
│   └── agents/                        # All agents as separate packages
│       │
│       ├── form_agent/                # Form-filling agent
│       │   ├── README.md              # Agent-specific documentation
│       │   ├── DEVELOPMENT-GUIDE.md   # Development guide for this agent
│       │   ├── agent.py               # Main agent implementation
│       │   ├── prompts.py             # AI agent prompts
│       │   ├── tools.py               # Agent tool belt
│       │   ├── models/                # Agent-specific database models
│       │   │   ├── base.py
│       │   │   └── request.py
│       │   └── services/              # Agent-specific services
│       │       └── validation.py      # Data validation
│       │
│       └── [future_agent]/            # Add new agents here
│           ├── README.md
│           ├── agent.py
│           ├── prompts.py
│           └── tools.py
```

## 🤖 Available Agents

### 1. Form Agent
**Purpose**: Conversational form-filling for OpenShift lab requests

**Features**:
- Guided conversation flow for collecting lab request information
- Real-time validation of user inputs
- Session-based state management
- Database integration for storing requests

**Documentation**: See [backend/agents/form_agent/README.md](backend/agents/form_agent/README.md)

### Future Agents
The architecture supports adding new agents easily. Each agent should be:
- Self-contained in its own package
- Have its own models, services, and documentation
- Register itself in [backend/main.py](backend/main.py)

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (recommended: Python 3.9+)
- **MySQL database** (version 8.0+)
- **Agno API key** (get from [Agno platform](https://agno.ai))
- **Node.js 18+** (for Agno UI frontend)
- **pnpm** (package manager for Node.js)

**For Development (Ollama)**:
- **Ollama** installed locally
- At least **8GB RAM** for local models

**For Production (OpenAI)**:
- **OpenAI API key** (get from [OpenAI platform](https://platform.openai.com))

### Installation

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
# Create database and user (MySQL)
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

Update your `.env` file with the database credentials.

#### 4. Initialize Database Tables

```bash
cd backend
python -c "from common.core.database import create_tables; create_tables()"
```

#### 5. Start the Backend Server

```bash
cd backend
python run.py
```

The AgentOS backend will be available at `http://localhost:8000`

#### 6. Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# Database connection test
cd backend
python -c "from common.core.database import test_connection; test_connection()"
```

## 🛠️ Development

### Adding a New Agent

To add a new agent to the system:

1. **Create agent package structure**:
```bash
mkdir -p backend/agents/new_agent/{models,services}
touch backend/agents/new_agent/{__init__.py,agent.py,prompts.py,tools.py,README.md}
```

2. **Implement the agent**:
   - Define agent logic in `agent.py`
   - Create prompts in `prompts.py`
   - Implement tools in `tools.py`
   - Add models in `models/` if needed
   - Document in `README.md`

3. **Register the agent** in [backend/main.py](backend/main.py):
```python
from agents.new_agent import new_agent

# Add to the available_agents list
available_agents = [
    form_agent.agent,
    new_agent.agent,  # Add your new agent here
]
```

4. **Update database** if needed:
   - Add new models in your agent's `models/` directory
   - Import and create tables in startup

### Code Organization

- **Common code**: Place shared utilities in `backend/common/`
- **Agent-specific code**: Keep in respective agent packages
- **Models**: Agent-specific models in agent's `models/` directory
- **Services**: Agent-specific services in agent's `services/` directory

### Testing

```bash
cd backend
pytest
```

## 🎨 Agno UI Interface

The application uses Agno UI (AG-UI) for the frontend interface, which provides:

- **Native Agno Integration**: Built specifically for Agno agents
- **ChatGPT-like Experience**: Familiar chat interface
- **Real-time Chat**: Instant message exchange
- **Multi-agent Support**: Switch between different agents
- **Markdown Support**: Rich text formatting in responses

### Frontend Setup

```bash
# Clone Agno UI repository
git clone https://github.com/ag-ui-protocol/ag-ui.git
cd ag-ui

# Install dependencies
cd typescript-sdk
pnpm install

# Build
cd ../integrations/agno
pnpm run build
```

## 🚀 Deployment

### Production Considerations

1. **Database**: Use a production MySQL instance with proper backups
2. **Session Storage**: Consider Redis for distributed session management
3. **Authentication**: Implement proper JWT token validation
4. **Security**: Add rate limiting, input sanitization, and CORS
5. **Monitoring**: Set up logging, metrics, and alerting
6. **Scaling**: Use load balancers for multiple backend instances

### Docker Deployment

```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["python", "run.py"]
```

## 📚 Documentation

- **Project Overview**: This file
- **Form Agent**: [backend/agents/form_agent/README.md](backend/agents/form_agent/README.md)
- **Development Guide**: [backend/agents/form_agent/DEVELOPMENT-GUIDE.md](backend/agents/form_agent/DEVELOPMENT-GUIDE.md)
- **API Documentation**: Available at `/docs` when server is running

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Manual Testing
1. Start the backend server
2. Start Agno UI frontend
3. Connect to the agent
4. Test conversation flows

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your agent or improvements
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check agent-specific documentation
- Review the development guides
- Open an issue on GitHub