"""
Data validation utilities for the OpenShift Partner Labs Agents application.
"""
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import pytz
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class FieldValidator:
    """Validates form fields according to business rules."""
    
    # Allowed values for specific fields
    ALLOWED_LEASE_DURATIONS = ["1d", "2d", "1w", "2w", "1m"]
    ALLOWED_APPLICATION_TYPES = ["workload", "infrastructure"]
    ALLOWED_REQUEST_TYPES = ["general", "engineering", "rosa", "nvidia", "virtualization", "ai"]
    ALLOWED_CLUSTER_SIZES = ["small", "medium", "large", "xl"]
    ALLOWED_CLOUD_PROVIDERS = ["aws", "gcp", "azure", "ibm"]
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not email or not isinstance(email, str):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_openshift_version(version: str) -> bool:
        """
        Validate OpenShift version format (4.y or 4.y.z).
        
        Args:
            version: Version string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not version or not isinstance(version, str):
            return False
        
        pattern = r'^4\.\d+(\.\d+)?$'
        return bool(re.match(pattern, version))
    
    @staticmethod
    def validate_timezone(timezone: str) -> bool:
        """
        Validate IANA timezone.
        
        Args:
            timezone: Timezone string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not timezone or not isinstance(timezone, str):
            return False
        
        try:
            pytz.timezone(timezone)
            return True
        except pytz.exceptions.UnknownTimeZoneError:
            return False
    
    @staticmethod
    def validate_lease_duration(duration: str) -> bool:
        """
        Validate lease duration.
        
        Args:
            duration: Duration string to validate
            
        Returns:
            True if valid, False otherwise
        """
        return duration in FieldValidator.ALLOWED_LEASE_DURATIONS
    
    @staticmethod
    def validate_application_type(app_type: str) -> bool:
        """
        Validate application type.
        
        Args:
            app_type: Application type to validate
            
        Returns:
            True if valid, False otherwise
        """
        return app_type in FieldValidator.ALLOWED_APPLICATION_TYPES
    
    @staticmethod
    def validate_request_type(request_type: str) -> bool:
        """
        Validate request type.
        
        Args:
            request_type: Request type to validate
            
        Returns:
            True if valid, False otherwise
        """
        return request_type in FieldValidator.ALLOWED_REQUEST_TYPES
    
    @staticmethod
    def validate_cluster_size(size: str) -> bool:
        """
        Validate cluster size.
        
        Args:
            size: Cluster size to validate
            
        Returns:
            True if valid, False otherwise
        """
        return size in FieldValidator.ALLOWED_CLUSTER_SIZES
    
    @staticmethod
    def validate_cloud_provider(provider: str) -> bool:
        """
        Validate cloud provider.
        
        Args:
            provider: Cloud provider to validate
            
        Returns:
            True if valid, False otherwise
        """
        return provider in FieldValidator.ALLOWED_CLOUD_PROVIDERS
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """
        Validate date format.
        
        Args:
            date_str: Date string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not date_str or not isinstance(date_str, str):
            return False
        
        try:
            datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_boolean(value: Any) -> bool:
        """
        Validate boolean value.
        
        Args:
            value: Value to validate
            
        Returns:
            True if valid, False otherwise
        """
        return isinstance(value, bool)
    
    @staticmethod
    def validate_required_string(value: str, min_length: int = 1) -> bool:
        """
        Validate required string field.
        
        Args:
            value: String to validate
            min_length: Minimum length required
            
        Returns:
            True if valid, False otherwise
        """
        return isinstance(value, str) and len(value.strip()) >= min_length

def validate_field(field_name: str, value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate a specific field based on its name and value.
    
    Args:
        field_name: Name of the field
        value: Value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Email fields
        if field_name.endswith("_email"):
            if not FieldValidator.validate_email(value):
                return False, f"Invalid email format for {field_name}"
        
        # OpenShift version
        elif field_name == "openshift_version":
            if not FieldValidator.validate_openshift_version(value):
                return False, "OpenShift version must be in format 4.y or 4.y.z"
        
        # Timezone
        elif field_name == "timezone":
            if not FieldValidator.validate_timezone(value):
                return False, "Invalid timezone. Must be a valid IANA timezone"
        
        # Lease duration
        elif field_name == "lease_duration":
            if not FieldValidator.validate_lease_duration(value):
                return False, f"Lease duration must be one of: {FieldValidator.ALLOWED_LEASE_DURATIONS}"
        
        # Application type
        elif field_name == "application_type":
            if not FieldValidator.validate_application_type(value):
                return False, f"Application type must be one of: {FieldValidator.ALLOWED_APPLICATION_TYPES}"
        
        # Request type
        elif field_name == "request_type":
            if not FieldValidator.validate_request_type(value):
                return False, f"Request type must be one of: {FieldValidator.ALLOWED_REQUEST_TYPES}"
        
        # Cluster size
        elif field_name == "cluster_size":
            if not FieldValidator.validate_cluster_size(value):
                return False, f"Cluster size must be one of: {FieldValidator.ALLOWED_CLUSTER_SIZES}"
        
        # Cloud provider
        elif field_name == "cloud_provider":
            if not FieldValidator.validate_cloud_provider(value):
                return False, f"Cloud provider must be one of: {FieldValidator.ALLOWED_CLOUD_PROVIDERS}"
        
        # Date fields
        elif field_name in ["desired_start_date", "timestamp", "request_eval_date"]:
            if not FieldValidator.validate_date(value):
                return False, f"Invalid date format for {field_name}"
        
        # Boolean fields
        elif field_name == "virtualization":
            if not FieldValidator.validate_boolean(value):
                return False, f"Virtualization must be a boolean value"
        
        # Required string fields
        elif field_name in [
            "company_name", "primary_contact_name", "project_name", 
            "description", "scope_of_work", "sponsor_email"
        ]:
            if not FieldValidator.validate_required_string(value):
                return False, f"{field_name} is required and cannot be empty"
        
        # Optional string fields
        elif field_name in ["secondary_contact_name", "secondary_contact_email", "notes", "cluster_requirements"]:
            if value is not None and not isinstance(value, str):
                return False, f"{field_name} must be a string or None"
        
        return True, None
        
    except Exception as e:
        logger.error(f"Validation error for field {field_name}: {e}")
        return False, f"Validation error: {str(e)}"

def validate_form_data(form_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate all form data.
    
    Args:
        form_data: Dictionary of form data
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Required fields
    required_fields = [
        "company_name", "primary_contact_name", "primary_contact_email",
        "sponsor_email", "project_name", "desired_start_date", "lease_duration",
        "timezone", "openshift_version", "application_type", "request_type",
        "cluster_size", "cloud_provider", "description", "scope_of_work"
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in form_data or not form_data[field]:
            errors.append(f"Required field '{field}' is missing")
    
    # Validate each field
    for field_name, value in form_data.items():
        is_valid, error_msg = validate_field(field_name, value)
        if not is_valid:
            errors.append(error_msg)
    
    # Check conditional requirements
    if form_data.get("virtualization") is True:
        if not form_data.get("cluster_requirements"):
            errors.append("cluster_requirements is required when virtualization is True")
    
    return len(errors) == 0, errors

