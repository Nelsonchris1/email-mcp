from typing import Any, List
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from .helper import (
    connect_to_email,
    format_email_message,
    send_email
)

mcp = FastMCP("email")

@mcp.tool()
async def get_recent_emails(folder: str = "INBOX", limit: int = 5) -> str:
    """Get recent emails from specified folder.
    
    Args:
        folder: Email folder to read from (default: INBOX)
        limit: Maximum number of emails to return (default: 5)
    """
    mail = connect_to_email()
    if not mail:
        return "Failed to connect to email server. Please check your credentials."
    
    try:
        mail.select(folder)
        _, message_numbers = mail.search(None, "ALL")
        email_list = message_numbers[0].split()
        
        # Get the most recent emails
        recent_emails = email_list[-limit:]
        emails = []
        
        for num in recent_emails:
            _, msg_data = mail.fetch(num, "(RFC822)")
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            emails.append(format_email_message(email_message))
        
        mail.close()
        mail.logout()
        
        return "\n\n---\n\n".join(emails)
        
    except Exception as e:
        return f"Error reading emails: {str(e)}"

@mcp.tool()
async def search_emails(query: str, folder: str = "INBOX", limit: int = 5) -> str:
    """Search emails in specified folder.
    
    Args:
        query: Search query
        folder: Email folder to search in (default: INBOX)
        limit: Maximum number of results to return (default: 5)
    """
    mail = connect_to_email()
    if not mail:
        return "Failed to connect to email server. Please check your credentials."
    
    try:
        mail.select(folder)
        
        _, message_numbers = mail.search(None, f'(OR SUBJECT "{query}" BODY "{query}")')
        email_list = message_numbers[0].split()
        
       
        recent_emails = email_list[-limit:]
        emails = []
        
        for num in recent_emails:
            _, msg_data = mail.fetch(num, "(RFC822)")
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            emails.append(format_email_message(email_message))
        
        mail.close()
        mail.logout()
        
        return "\n\n---\n\n".join(emails)
        
    except Exception as e:
        return f"Error searching emails: {str(e)}"

@mcp.tool()
async def send_email_message(to_email: str, subject: str, body: str) -> str:
    """Send an email to a specified recipient.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body content
    """
    if send_email(to_email, subject, body):
        return f"Email sent successfully to {to_email}"
    else:
        return "Failed to send email. Please check your credentials and try again."

if __name__ == "__main__":
    mcp.run(transport="stdio") 