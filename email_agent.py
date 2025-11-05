import os
import re
from typing import Dict

from mailjet_rest import Client
from agents import Agent, function_tool


def is_valid_email(email: str) -> bool:
    """Validate email format using regular expressions."""
    if not email or not email.strip():
        return False
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email.strip()) is not None


# Global variable to store recipient email
_recipient_email = None


def set_recipient_email(email: str):
    """Set the recipient email address."""
    global _recipient_email
    _recipient_email = email if email and is_valid_email(email) else None

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send an email with the given subject and HTML body """
    global _recipient_email

    # If no valid recipient email is set, return without sending
    if not _recipient_email:
        return {"status": "skipped", "message": "No recipient email provided"}

    mailjet = Client(
        auth=(os.environ.get('MAILJET_API_KEY'), os.environ.get('MAILJET_SECRET_KEY')),
        version='v3.1'
    )

    from_email = "joe.lazo.flores@gmail.com"  # put your verified sender here
    to_email = _recipient_email
    
    data = {
        'Messages': [
            {
                "From": {
                    "Email": from_email,
                    "Name": "Email Agent"
                },
                "To": [
                    {
                        "Email": to_email
                    }
                ],
                "Subject": subject,
                "HTMLPart": html_body
            }
        ]
    }
    
    result = mailjet.send.create(data=data)
    print("Email response", result.status_code)
    print("Email response body", result.json())
    return {"status": "success"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
