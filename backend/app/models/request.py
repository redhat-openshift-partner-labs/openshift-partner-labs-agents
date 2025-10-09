"""
Database model for lab requests.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, TIMESTAMP
from sqlalchemy.sql import func

from .base import Base

class Request(Base):
    """
    Database model for lab requests.
    
    This table stores all the information collected through the AI agent
    conversation for OpenShift lab requests.
    """
    __tablename__ = "requests"
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Auto-generated fields
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
    request_state = Column(String(50), nullable=False, default='pending')
    request_eval_date = Column(DateTime, nullable=False, default=datetime.now)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    
    # User authentication (pre-filled from OIDC)
    email_address = Column(String(255), nullable=False)
    
    # Company information
    company_name = Column(String(255), nullable=False)
    primary_contact_name = Column(String(255), nullable=False)
    primary_contact_email = Column(String(255), nullable=False)
    
    # Optional secondary contact
    secondary_contact_name = Column(String(255), nullable=True)
    secondary_contact_email = Column(String(255), nullable=True)
    
    # Sponsor information
    sponsor_email = Column(String(255), nullable=False)
    
    # Project details
    project_name = Column(String(255), nullable=False)
    desired_start_date = Column(DateTime, nullable=False)
    lease_duration = Column(String(10), nullable=False)  # "1d", "2d", "1w", "2w", "1m"
    timezone = Column(String(100), nullable=False)  # IANA timezone
    
    # Technical specifications
    openshift_version = Column(String(20), nullable=False)  # Format: 4.y or 4.y.z
    virtualization = Column(Boolean, nullable=False, default=False)
    cluster_requirements = Column(Text, nullable=True)  # Required only if virtualization=True
    application_type = Column(String(50), nullable=False)  # "workload" or "infrastructure"
    request_type = Column(String(50), nullable=False)  # "general", "engineering", "rosa", "nvidia", "virtualization", "ai"
    cluster_size = Column(String(20), nullable=False)  # "small", "medium", "large", "xl"
    cloud_provider = Column(String(50), nullable=False)  # "aws", "gcp", "azure", "ibm"
    
    # Project description
    description = Column(Text, nullable=False)
    scope_of_work = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Request(id={self.id}, company_name='{self.company_name}', project_name='{self.project_name}')>"
    
    def to_dict(self):
        """Convert the model to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'request_state': self.request_state,
            'request_eval_date': self.request_eval_date.isoformat() if self.request_eval_date else None,
            'email_address': self.email_address,
            'company_name': self.company_name,
            'primary_contact_name': self.primary_contact_name,
            'primary_contact_email': self.primary_contact_email,
            'secondary_contact_name': self.secondary_contact_name,
            'secondary_contact_email': self.secondary_contact_email,
            'sponsor_email': self.sponsor_email,
            'project_name': self.project_name,
            'desired_start_date': self.desired_start_date.isoformat() if self.desired_start_date else None,
            'lease_duration': self.lease_duration,
            'timezone': self.timezone,
            'openshift_version': self.openshift_version,
            'virtualization': self.virtualization,
            'cluster_requirements': self.cluster_requirements,
            'application_type': self.application_type,
            'request_type': self.request_type,
            'cluster_size': self.cluster_size,
            'cloud_provider': self.cloud_provider,
            'description': self.description,
            'scope_of_work': self.scope_of_work,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

