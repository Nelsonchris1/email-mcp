import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# Email server settings
EMAIL_SERVER = "imap.gmail.com" 
EMAIL_PORT = 993
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def connect_to_email() -> imaplib.IMAP4_SSL | None:
    """Connect to email server with credentials from environment variables"""
    try:
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASSWORD")
        
        if not email_user or not email_pass:
            return None
            
        mail = imaplib.IMAP4_SSL(EMAIL_SERVER, EMAIL_PORT)
        mail.login(email_user, email_pass)
        return mail
    except Exception as e:
        print(f"Error connecting to email: {e}")
        return None

def send_email(to_email: str, subject: str, body: str) -> bool:
    """Send an email using SMTP.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body content
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASSWORD")
        
        if not email_user or not email_pass:
            return False
            
        
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        
        msg.attach(MIMEText(body, 'plain'))
        
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
            
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def decode_email_subject(subject: str) -> str:
    """Decode email subject from various encodings"""
    decoded_chunks = decode_header(subject)
    subject = ""
    for chunk, encoding in decoded_chunks:
        if isinstance(chunk, bytes):
            if encoding:
                subject += chunk.decode(encoding)
            else:
                subject += chunk.decode()
        else:
            subject += chunk
    return subject

def format_email_message(email_message: email.message.Message) -> str:
    """Format email message into readable text"""
    subject = decode_email_subject(email_message["subject"] or "No Subject")
    from_addr = email_message["from"] or "Unknown Sender"
    date = email_message["date"] or "No Date"
    
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    body = "Could not decode email body"
                break
    else:
        try:
            body = email_message.get_payload(decode=True).decode()
        except:
            body = "Could not decode email body"
    
    return f"""
From: {from_addr}
Subject: {subject}
Date: {date}
---
{body}
""" 