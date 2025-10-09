"""
Run script for the OpenShift Partner Labs Agents backend.
"""
from app.core.config import config
from app.main import agent_os, app

if __name__ == "__main__":
    agent_os.serve(
        app=app,
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG
    )
