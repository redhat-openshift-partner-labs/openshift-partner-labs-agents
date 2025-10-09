"""
AgentOS application for the OpenShift Partner Labs Agents.
"""
import logging
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI

from app.core.config import config
from app.core.database import test_connection, create_tables
from app.agents.form_agent import form_agent

# Configure logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

def create_agent_os():
    """Create and configure the AgentOS with AG-UI interface."""
    try:
        # Create AgentOS with our form-filling agent
        agent_os = AgentOS(
            id="openshift-partner-labs",
            description="AI-powered form-filling agent for OpenShift lab requests",
            agents=[form_agent.agent],
            interfaces=[
                AGUI(agent=form_agent.agent)
            ]
        )
        
        return agent_os
        
    except Exception as e:
        logger.error(f"Error creating AgentOS: {e}")
        raise

# Create AgentOS instance
agent_os = create_agent_os()
app = agent_os.get_app()

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    try:
        # Validate configuration
        config.validate_config()
        
        # Test database connection
        if not test_connection():
            logger.warning("Database connection failed - some features may not work")
        else:
            logger.info("Database connection successful")
        
        # Create tables if they don't exist
        create_tables()
        
        logger.info("AgentOS startup completed")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
