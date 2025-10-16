"""
System prompts for the OpenShift Partner Labs Agents application.
"""
from typing import Dict, Any

def get_system_prompt(form_data: Dict[str, Any]) -> str:
    """
    Generate the system prompt for the AI agent.
    
    Args:
        form_data: Current form data state
        
    Returns:
        System prompt string
    """
    form_data_json = str(form_data) if form_data else "{}"
    
    return f"""
You are a helpful OpenShift lab request assistant. Your job is to collect information from users to create lab requests.

**IMPORTANT BEHAVIOR:**
- Be proactive and ask for ONE piece of information at a time
- Use the tools to store and validate information
- Don't ask for confirmation unless you're ready to submit
- Guide users through the process step by step

**Current Form Data:**
{form_data_json}

**Required Information to Collect:**
1. User's email address
2. Company name  
3. Contact person's name
4. Contact person's email
5. OpenShift version (like 4.15 or 4.16)
6. Cluster size (small, medium, large, xl)
7. Use case description
8. Any additional requirements or notes

**Process:**
1. Ask for one piece of information at a time
2. Use update_form_data to store the information
3. Use validate_data to check email formats
4. Use get_form_summary to show progress
5. Use check_form_completeness to verify all fields are filled
6. Only submit when everything is complete

**Be conversational and helpful. Don't ask for confirmations unless you're ready to submit the form.**
"""

def get_welcome_message() -> str:
    """Get the initial welcome message for new conversations."""
    return """
Hello! I'm here to help you request a new OpenShift lab environment. I'll guide you through a few questions to collect the necessary information for your request.

Let's start with the basics - what would you like to name your project?
"""

def get_completion_message(request_id: int) -> str:
    """
    Get the completion message after successful form submission.
    
    Args:
        request_id: The ID of the submitted request
        
    Returns:
        Completion message
    """
    return f"""
Perfect! Your OpenShift lab request has been successfully submitted. 

**Request ID:** {request_id}

Your request is now in the system and will be reviewed by our team. You should receive a confirmation email shortly with next steps.

Is there anything else I can help you with?
"""

def get_validation_error_message(field_name: str, error_message: str) -> str:
    """
    Get a message for validation errors.
    
    Args:
        field_name: Name of the field that failed validation
        error_message: Specific error message
        
    Returns:
        Error message for the user
    """
    return f"""
I'm sorry, but there seems to be an issue with the {field_name} you provided.

**Error:** {error_message}

Could you please provide a valid value for {field_name}?
"""

def get_form_summary_prompt(form_data: Dict[str, Any]) -> str:
    """
    Generate a summary of the form data for user confirmation.
    
    Args:
        form_data: Current form data
        
    Returns:
        Form summary string
    """
    summary_lines = ["Here's a summary of the information you've provided:\n"]
    
    # Group fields by category
    company_info = {
        "Company Name": form_data.get("company_name"),
        "Primary Contact": form_data.get("primary_contact_name"),
        "Primary Contact Email": form_data.get("primary_contact_email"),
        "Secondary Contact": form_data.get("secondary_contact_name"),
        "Secondary Contact Email": form_data.get("secondary_contact_email"),
        "Sponsor Email": form_data.get("sponsor_email"),
    }
    
    project_info = {
        "Project Name": form_data.get("project_name"),
        "Desired Start Date": form_data.get("desired_start_date"),
        "Lease Duration": form_data.get("lease_duration"),
        "Timezone": form_data.get("timezone"),
    }
    
    technical_info = {
        "OpenShift Version": form_data.get("openshift_version"),
        "Virtualization": form_data.get("virtualization"),
        "Cluster Requirements": form_data.get("cluster_requirements"),
        "Application Type": form_data.get("application_type"),
        "Request Type": form_data.get("request_type"),
        "Cluster Size": form_data.get("cluster_size"),
        "Cloud Provider": form_data.get("cloud_provider"),
    }
    
    description_info = {
        "Description": form_data.get("description"),
        "Scope of Work": form_data.get("scope_of_work"),
        "Notes": form_data.get("notes"),
    }
    
    # Add sections
    summary_lines.append("**Company Information:**")
    for key, value in company_info.items():
        if value:
            summary_lines.append(f"- {key}: {value}")
    
    summary_lines.append("\n**Project Information:**")
    for key, value in project_info.items():
        if value:
            summary_lines.append(f"- {key}: {value}")
    
    summary_lines.append("\n**Technical Specifications:**")
    for key, value in technical_info.items():
        if value:
            summary_lines.append(f"- {key}: {value}")
    
    summary_lines.append("\n**Project Details:**")
    for key, value in description_info.items():
        if value:
            summary_lines.append(f"- {key}: {value}")
    
    summary_lines.append("\n**Please review this information carefully. Does everything look correct?**")
    
    return "\n".join(summary_lines)
