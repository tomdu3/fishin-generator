import os
import smtplib
from email.message import EmailMessage
from jinja2 import Template

def generate_email_content(template_html, tracking_url, tracking_pixel_url):
    # Render tracking_url into the template
    jinja_template = Template(template_html)
    rendered_html = jinja_template.render(tracking_url=tracking_url)
    
    # Append tracking pixel
    rendered_html += f'<img src="{tracking_pixel_url}" width="1" height="1" alt="" style="display:none;" />'
    
    return rendered_html

def send_phishing_email(target_email, subject, html_content):
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')
    sender_email = os.environ.get('SENDER_EMAIL', 'security-test@company.com')
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = target_email
    msg.set_content("Please enable HTML to view this message.")
    msg.add_alternative(html_content, subtype='html')

    if smtp_server and smtp_user and smtp_pass:
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            print(f"Email sent to {target_email} via SMTP.")
            return True
        except Exception as e:
            print(f"Failed to send email to {target_email}: {e}")
            return False
    else:
        # Dry Run Mode
        print("\n" + "="*50)
        print("DRY RUN MODE - NO SMTP CREDENTIALS CONFIGURED")
        print(f"To: {target_email}")
        print(f"From: {sender_email}")
        print(f"Subject: {subject}")
        print("-" * 50)
        print(html_content)
        print("="*50 + "\n")
        return True
