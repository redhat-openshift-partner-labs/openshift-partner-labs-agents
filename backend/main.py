"""
AgentOS application for the OpenShift Partner Labs Agents.

This is the main entry point for the multi-agent system.
It dynamically loads all available agents and registers them with AgentOS.
"""
import logging
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI

from common.core.config import config
from common.core.database import test_connection, create_tables

# Import all agents
from agents.form_agent import form_agent

# Configure logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

def create_agent_os():
    """Create and configure the AgentOS with all available agents."""
    try:
        # Collect all agents
        available_agents = [
            form_agent.agent,
            # Add more agents here as they are developed
        ]

        logger.info(f"Initializing AgentOS with {len(available_agents)} agent(s)")

        # Create AgentOS with all agents
        # Each agent will have its own AGUI interface
        agent_os = AgentOS(
            id="openshift-partner-labs",
            description="AI-powered multi-agent system for OpenShift Partner Labs",
            agents=available_agents,
            interfaces=[
                AGUI(agent=agent.agent if hasattr(agent, 'agent') else agent)
                for agent in available_agents
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

        logger.info("AgentOS startup completed successfully")
        logger.info(f"Available agents: {[agent.name for agent in agent_os.agents]}")

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
