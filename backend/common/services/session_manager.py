"""
Session management for the OpenShift Partner Labs Agents application.
"""
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class SessionData:
    """Data structure for session information."""
    session_id: str
    user_email: str
    form_data: Dict[str, Any]
    created_at: datetime
    last_accessed: datetime
    is_active: bool = True

class SessionManager:
    """
    Manages user sessions and form data state.
    
    In production, this should be replaced with Redis or another
    persistent session store.
    """
    
    def __init__(self):
        # In-memory storage for development
        # In production, use Redis or database
        self._sessions: Dict[str, SessionData] = {}
        self._session_expiry_hours = 24
    
    def create_session(self, user_email: str) -> str:
        """
        Create a new session for a user.
        
        Args:
            user_email: Email address of the user
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        session_data = SessionData(
            session_id=session_id,
            user_email=user_email,
            form_data={},
            created_at=now,
            last_accessed=now
        )
        
        self._sessions[session_id] = session_data
        logger.info(f"Created new session {session_id} for user {user_email}")
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionData]:
        """
        Get session data by session ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data or None if not found/expired
        """
        if session_id not in self._sessions:
            return None
        
        session = self._sessions[session_id]
        
        # Check if session is expired
        if self._is_session_expired(session):
            self.delete_session(session_id)
            return None
        
        # Update last accessed time
        session.last_accessed = datetime.now()
        
        return session
    
    def update_form_data(self, session_id: str, field_name: str, value: Any) -> bool:
        """
        Update a field in the session's form data.
        
        Args:
            session_id: Session identifier
            field_name: Name of the field to update
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.form_data[field_name] = value
        session.last_accessed = datetime.now()
        
        logger.info(f"Updated field '{field_name}' in session {session_id}")
        return True
    
    def get_form_data(self, session_id: str) -> Dict[str, Any]:
        """
        Get all form data for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Form data dictionary
        """
        session = self.get_session(session_id)
        if not session:
            return {}
        
        return session.form_data.copy()
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if successful, False otherwise
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Deleted session {session_id}")
            return True
        return False
    
    def _is_session_expired(self, session: SessionData) -> bool:
        """
        Check if a session has expired.
        
        Args:
            session: Session data
            
        Returns:
            True if expired, False otherwise
        """
        expiry_time = session.last_accessed + timedelta(hours=self._session_expiry_hours)
        return datetime.now() > expiry_time
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions.
        
        Returns:
            Number of sessions cleaned up
        """
        expired_sessions = []
        
        for session_id, session in self._sessions.items():
            if self._is_session_expired(session):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self._sessions[session_id]
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        
        return len(expired_sessions)
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get a summary of the session data.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session summary
        """
        session = self.get_session(session_id)
        if not session:
            return {}
        
        return {
            'session_id': session.session_id,
            'user_email': session.user_email,
            'form_data': session.form_data,
            'created_at': session.created_at.isoformat(),
            'last_accessed': session.last_accessed.isoformat(),
            'is_active': session.is_active,
            'field_count': len(session.form_data)
        }

# Global session manager instance
session_manager = SessionManager()



