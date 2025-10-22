"""
Simple Email Service for Personal Delivery

A lightweight SMTP service for sending emails.
Just the essentials - no complex templating or multi-user features.
"""

import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict

import markdown
from fastmcp.utilities.logging import get_logger
from jinja2 import Environment, FileSystemLoader, select_autoescape


class EmailService:
    """Simple email service for personal delivery."""

    def __init__(self, email_settings):
        """Initialize with email settings."""
        self.logger = get_logger("EmailService")

        # Handle both dict and EmailSettings object
        if isinstance(email_settings, dict):
            # Dictionary input
            self.server = email_settings.get("server", "localhost")
            self.port = email_settings.get("port", 587)
            self.use_tls = email_settings.get("use_tls", True)
            self.use_ssl = email_settings.get("use_ssl", False)
            self.username = email_settings.get("username", "")
            self.password = email_settings.get("password", "")
            self.from_email = email_settings.get("from_email", "newsletter@localhost")
            self.from_name = email_settings.get("from_name", "Personal Agent")
        else:
            # EmailSettings object
            self.server = email_settings.server
            self.port = email_settings.port
            self.use_tls = email_settings.use_tls
            self.use_ssl = getattr(email_settings, "use_ssl", False)
            self.username = email_settings.username
            self.password = email_settings.password
            self.from_email = email_settings.from_email
            self.from_name = email_settings.from_name

        # Setup Jinja2 for templates
        template_dir = Path(__file__).parent.parent / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )

        # Add markdown filter
        self.jinja_env.filters["markdown"] = lambda text: (
            markdown.markdown(text) if text else ""
        )

    def create_outfit_email_html(
        self, outfit_recommendation: str, season: str, date_str: str
    ) -> str:
        """
        Create HTML email for outfit recommendation.
        
        Args:
            outfit_recommendation: The outfit text
            season: Current season (fall, winter, spring, summer)
            date_str: Formatted date string
            
        Returns:
            HTML content for email
        """
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #4a90e2;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            color: #2c3e50;
            font-size: 28px;
        }}
        .season-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            margin-top: 10px;
            font-weight: 600;
        }}
        .outfit-content {{
            white-space: pre-wrap;
            font-size: 15px;
            line-height: 1.8;
            text-align: left;
        }}
        .footer {{
            text-align: center;
            color: #95a5a6;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👔 Your Personalized Outfit</h1>
            <div class="season-badge">{season.upper()} COLLECTION</div>
            <div style="color: #7f8c8d; font-size: 14px; margin-top: 10px;">{date_str}</div>
        </div>
        
        <div class="outfit-content">
{outfit_recommendation}
        </div>
        
        <div class="footer">
            Created by Your Personal AI Stylist<br>
            Powered by Outfit Inspiration Agent
        </div>
    </div>
</body>
</html>"""

    def send_outfit_email(
        self, outfit_recommendation: str, season: str, date_str: str, subject: str = ""
    ) -> Dict:
        """
        Send an outfit recommendation email.
        
        Args:
            outfit_recommendation: The outfit text
            season: Current season
            date_str: Formatted date string
            subject: Optional custom subject
            
        Returns:
            Dict: Success status and details
        """
        # Create HTML content
        html_content = self.create_outfit_email_html(outfit_recommendation, season, date_str)
        
        # Create text content
        text_content = f"""Your Personalized Outfit - {date_str}
                        {season.upper()} COLLECTION
                        {'='*50}

                        {outfit_recommendation}

                        ---
                        Created by Your Personal AI Stylist
                        """
        
        # Set subject
        email_subject = subject or f"👔 Your Personalized {season.title()} Outfit - {date_str}"
        
        # Send using the simple email method
        return self.send_simple_email(html_content, text_content, email_subject)

    def send_simple_email(
        self, html_content: str, text_content: str, subject: str
    ) -> Dict:
        """
        Send a simple email with HTML and text versions.
        
        Args:
            html_content: HTML version of email
            text_content: Plain text version of email
            subject: Email subject line
            
        Returns:
            Dict: Success status and details
        """
        try:
            # Create email
            msg = MIMEMultipart("alternative")
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = self.from_email  # Always send to yourself
            msg["Subject"] = subject

            # Attach both versions
            text_part = MIMEText(text_content, "plain", "utf-8")
            html_part = MIMEText(html_content, "html", "utf-8")
            msg.attach(text_part)
            msg.attach(html_part)

            # Send email - handle both SSL and TLS
            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.server, self.port, timeout=30)
                self.logger.debug(f"Connected via SSL to {self.server}:{self.port}")
            else:
                server = smtplib.SMTP(self.server, self.port, timeout=30)
                if self.use_tls:
                    server.starttls()
                    self.logger.debug(f"Started TLS on {self.server}:{self.port}")

            # Login and send
            if self.username and self.password:
                server.login(self.username, self.password)
                self.logger.debug("SMTP login successful")

            server.send_message(msg)
            server.quit()

            self.logger.info("Email sent successfully")
            return {"success": True, "message": "Email delivered successfully"}

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return {"success": False, "error": str(e)}
