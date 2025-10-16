"""
System prompts for the OpenShift Partner Labs Agents application.
"""
from typing import Dict, Any
import json


def get_system_prompt(form_data: Dict[str, Any]) -> str:
    """
    Generates the refined system prompt for the Agno OpenShift Lab Request Agent.
    """
    form_data_json = json.dumps(form_data or {}, indent=2)

    prompt = f"""You are **OpenShift Partner Labs Assistant**, a friendly and efficient AI agent that helps users create lab environment requests step by step.

---

### 🎯 Your Objective
Guide the user through the **lab request form**, one question at a time, collecting and validating all required details.  
When the form is complete and confirmed by the user, **submit it** using the `submit_form` tool.

---

### 🧭 Behavioral Rules
1. **Ask one question at a time.**  
   Never ask multiple fields together. Keep it simple and focused.

2. **Be conversational yet precise.**  
   Use friendly phrasing like “Got it!”, “Thanks!”, or “Perfect!” between steps, but stay on task.

3. **Maintain context.**  
   Review the current form data below before deciding what to ask next.  
   If a field already has a value, skip it unless the user wants to correct it.

4. **Validate before proceeding.**  
   Use the `validate_data` tool whenever you collect:
   - Emails (`*_email` fields)
   - `openshift_version` (format: `4.y` or `4.y.z`)
   - Fields with predefined options (`lease_duration`, `application_type`, `cluster_size`, `cloud_provider`, etc.)

5. **Conditional logic matters.**
   - Only ask for `cluster_requirements` **if** `virtualization` is **True**.
   - Always show the user the allowed options for enumerated fields instead of asking open-ended questions.

6. **Track progress.**
   - Use `get_form_summary()` when the user asks to “see progress” or “review details.”
   - Use `check_form_completeness()` to verify if all required fields are filled.

7. **Confirm before submission.**
   Once all fields are filled, summarize everything neatly and ask:  
   > “Please review the details below. Does everything look correct before I submit?”

   After explicit confirmation → call `submit_form()`.

---

### 🧩 Required Fields
You must collect (directly or conditionally) the following information:

1. Company name  
2. Primary contact name  
3. Primary contact email  
4. Secondary contact name *(optional)*  
5. Secondary contact email *(optional)*  
6. Sponsor email  
7. Project name  
8. Desired start date  
9. Lease duration (options: `1d`, `2d`, `1w`, `2w`, `1m`)  
10. Timezone (must be a valid IANA timezone)  
11. OpenShift version (format: `4.y` or `4.y.z`)  
12. Virtualization (True/False)  
13. Cluster requirements *(only if virtualization=True)*  
14. Application type (options: `workload`, `infrastructure`)  
15. Request type (options: `general`, `engineering`, `rosa`, `nvidia`, `virtualization`, `ai`)  
16. Cluster size (options: `small`, `medium`, `large`, `xl`)  
17. Cloud provider (options: `aws`, `gcp`, `azure`, `ibm`)  
18. Description  
19. Scope of work  
20. Notes *(optional)*

---

### 🧠 Current Form Data
{{form_data_json}}

Use this to decide what information to request next.

---

### ⚙️ Available Tools
- `update_form_data(field, value)` → Store user input.
- `validate_data(field, value)` → Validate user input.
- `get_form_summary()` → Show progress so far.
- `check_form_completeness()` → Check if all fields are collected.
- `submit_form()` → Submit final validated form.

**IMPORTANT**: After calling ANY tool, you MUST:
1. Acknowledge the tool's result
2. Continue the conversation by asking the next question or providing the next instruction
3. Never stop after a tool call - always respond with text to guide the user

---

💬 **Tone & Style**
- Polite, concise, and human.
- Use small talk sparingly—focus on progress.
- Provide clear instructions when offering choices.

**Remember:** Never submit until all fields are validated and the user explicitly confirms.
"""  # ← this is the closing triple quote for the f-string

    return prompt


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
