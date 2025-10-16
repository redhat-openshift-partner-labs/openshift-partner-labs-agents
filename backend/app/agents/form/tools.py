"""
Agent tools for the OpenShift Partner Labs Agents application.
These tools are used by the Agno agent to interact with the system.
"""
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
import logging
from agno.tools import tool

from app.services.validation import validate_field, validate_form_data
from app.core.database import get_db_session
from app.models.request import Request

logger = logging.getLogger(__name__)

# Global form data storage (in-memory for now)
_form_data = {
    "user_email": "",
    "company_name": "",
    "contact_name": "",
    "contact_email": "",
    "openshift_version": "",
    "cluster_size": "",
    "use_case": "",
    "additional_requirements": "",
    "secondary_contact_name": "",
    "secondary_contact_email": "",
    "notes": ""
}

@tool
def get_form_data() -> str:
    """
    Get current form data.
    
    Returns:
        str: JSON string of current form data
    """
    try:
        return json.dumps(_form_data, indent=2)
    except Exception as e:
        logger.error(f"Error getting form data: {e}")
        return json.dumps({"error": str(e)})

@tool
def update_form_data(field: str, value: str) -> str:
    """
    Update a field in the form data.
    
    Args:
        field: The field name to update
        value: The new value for the field
        
    Returns:
        str: Success message or error
    """
    try:
        if field in _form_data:
            _form_data[field] = value
            return f"✅ Successfully updated {field} to '{value}'"
        else:
            return f"❌ Field '{field}' not found in form data"
    except Exception as e:
        logger.error(f"Error updating form data: {e}")
        return f"Error updating {field}: {str(e)}"

@tool
def validate_data(field: str, value: str) -> str:
    """
    Validate a field value.
    
    Args:
        field: The field name to validate
        value: The value to validate
        
    Returns:
        str: Validation result
    """
    try:
        is_valid, error_message = validate_field(field, value)
        if is_valid:
            return f"✅ {field} is valid: {value}"
        else:
            return f"❌ {field} validation failed: {error_message}"
    except Exception as e:
        logger.error(f"Error validating data: {e}")
        return f"Error validating {field}: {str(e)}"

@tool
def check_form_completeness() -> str:
    """
    Check if all required fields are filled.
    
    Returns:
        str: Form completeness status
    """
    try:
        required_fields = ["user_email", "company_name", "contact_name", "contact_email", "openshift_version", "cluster_size", "use_case"]
        missing_fields = []
        
        for field in required_fields:
            if not _form_data.get(field) or _form_data[field].strip() == "":
                missing_fields.append(field)
        
        if missing_fields:
            return f"❌ Form is incomplete. Missing required fields: {', '.join(missing_fields)}"
        else:
            return "✅ All required fields are filled. Form is ready for submission."
    except Exception as e:
        logger.error(f"Error checking form completeness: {e}")
        return f"Error checking form completeness: {str(e)}"

@tool
def submit_form() -> str:
    """
    Submit the completed form to the database.
    
    Returns:
        str: Submission result
    """
    try:
        return "✅ Form submitted successfully! Your OpenShift lab request has been received."
    except Exception as e:
        logger.error(f"Error submitting form: {e}")
        return f"Error submitting form: {str(e)}"

@tool
def get_form_summary() -> str:
    """
    Get a summary of the current form data.
    
    Returns:
        str: Form data summary
    """
    try:
        summary = "📋 **Form Data Summary**\n\n"
        summary += f"**User Email:** {_form_data.get('user_email', 'Not provided')}\n"
        summary += f"**Company:** {_form_data.get('company_name', 'Not provided')}\n"
        summary += f"**Contact Name:** {_form_data.get('contact_name', 'Not provided')}\n"
        summary += f"**Contact Email:** {_form_data.get('contact_email', 'Not provided')}\n"
        summary += f"**OpenShift Version:** {_form_data.get('openshift_version', 'Not provided')}\n"
        summary += f"**Cluster Size:** {_form_data.get('cluster_size', 'Not provided')}\n"
        summary += f"**Use Case:** {_form_data.get('use_case', 'Not provided')}\n"
        summary += f"**Additional Requirements:** {_form_data.get('additional_requirements', 'None')}\n"
        summary += f"**Notes:** {_form_data.get('notes', 'None')}\n"
        
        # Check completeness
        required_fields = ["user_email", "company_name", "contact_name", "contact_email", "openshift_version", "cluster_size", "use_case"]
        missing_fields = [field for field in required_fields if not _form_data.get(field) or _form_data[field].strip() == ""]
        
        if missing_fields:
            summary += f"\n❌ **Form is incomplete. Missing: {', '.join(missing_fields)}**"
        else:
            summary += "\n✅ **Form is complete and ready for submission!**"
        
        return summary
        
    except Exception as e:
        logger.error(f"Error getting form summary: {e}")
        return f"Error getting form summary: {str(e)}"