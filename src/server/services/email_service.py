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
        # Season-specific color schemes
        season_colors = {
            "winter": {
                "bg": "#E3F2FD",           # Soft icy blue
                "bubble": "rgba(255, 255, 255, 0.75)",  # Transparent white
                "accent": "#1976D2",        # Deep blue
                "name": "Winter"
            },
            "spring": {
                "bg": "#F1F8E9",           # Soft sage green
                "bubble": "rgba(255, 255, 255, 0.75)",
                "accent": "#388E3C",        # Forest green
                "name": "Spring"
            },
            "summer": {
                "bg": "#FFF8E1",           # Warm cream/sunshine
                "bubble": "rgba(255, 255, 255, 0.75)",
                "accent": "#F57C00",        # Warm orange
                "name": "Summer"
            },
            "fall": {
                "bg": "#FBE9E7",           # Warm peachy terracotta
                "bubble": "rgba(255, 255, 255, 0.75)",
                "accent": "#D84315",        # Deep rust/terracotta
                "name": "Fall"
            }
        }
        colors = season_colors.get(season.lower(), season_colors["fall"])
        
        # Split recommendation into paragraphs for better visual separation
        paragraphs = [p.strip() for p in outfit_recommendation.split('\n\n') if p.strip()]
        
        # Section headings that match the expected structure
        headings = [
            "The Look",
            "The Details", 
            "Where to Shop",
            "Switch It Up"  # For alternatives
        ]
        
        # Create HTML message bubbles for each paragraph
        bubbles_html = ""
        for i, paragraph in enumerate(paragraphs):
            heading = headings[i] if i < len(headings) else f"Part {i+1}"
            bubbles_html += f"""
            <div class="message-bubble">
                <div class="bubble-heading">{heading}</div>
                <div class="bubble-text">{paragraph}</div>
            </div>"""
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', sans-serif;
            margin: 0;
            padding: 0;
            background-color: {colors['bg']};
            line-height: 1.4;
        }}
        .messages-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: {colors['bg']};
            min-height: 100vh;
        }}
        .header {{
            background-color: #ffffff;
            padding: 20px;
            text-align: center;
            border-bottom: 1px solid #e5e5ea;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        .contact-name {{
            font-size: 16px;
            font-weight: 600;
            color: #000000;
            margin: 0 0 4px 0;
        }}
        .contact-subtitle {{
            font-size: 12px;
            color: #8e8e93;
            margin: 0;
        }}
        .messages-area {{
            padding: 20px 16px 80px 16px;
        }}
        .timestamp {{
            text-align: center;
            color: #8e8e93;
            font-size: 12px;
            margin: 20px 0 15px 0;
            font-weight: 400;
        }}
        .message-bubble {{
            background-color: {colors['bubble']};
            border-radius: 20px;
            padding: 16px 18px;
            margin: 10px 0;
            max-width: 90%;
            position: relative;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.6);
        }}
        .bubble-heading {{
            font-size: 10px;
            font-weight: 600;
            color: {colors['accent']};
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            opacity: 0.85;
        }}
        .bubble-text {{
            font-size: 15px;
            color: #1c1c1e;
            line-height: 1.5;
            margin: 0;
        }}
    </style>
</head>
<body>
    <div class="messages-container">
        <div class="header">
            <div class="contact-name">Your Stylist</div>
            <div class="contact-subtitle">{season.title()} Vibes</div>
        </div>
        
        <div class="messages-area">
            <div class="timestamp">{date_str}</div>
{bubbles_html}
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
        
        # Set subject - text message style
        email_subject = subject or f"💬 Your Stylist"
        
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
