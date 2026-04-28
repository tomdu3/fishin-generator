import os
import smtplib
from email.message import EmailMessage
from jinja2 import Template

def generate_email_content(template_html, tracking_url, tracking_pixel_url):
    # 1. Render the template body with available variables
    jinja_template = Template(template_html)
    rendered_body = jinja_template.render(
        tracking_url=tracking_url,
        tracking_pixel_url=tracking_pixel_url
    )
    
    # 2. Wrap in responsive base template
    base_template_path = os.path.join(os.path.dirname(__file__), 'templates', 'email_base.html')
    try:
        with open(base_template_path, 'r', encoding='utf-8') as f:
            base_html = f.read()
        
        base_jinja = Template(base_html)
        rendered_html = base_jinja.render(content=rendered_body)
    except Exception as e:
        print(f"Warning: Could not load email_base.html: {e}. Using raw body.")
        rendered_html = rendered_body

    # 3. Smart Pixel Insertion (ensure it's not already there and put it before </body>)
    if tracking_pixel_url not in rendered_html:
        pixel_tag = f'<img src="{tracking_pixel_url}" width="1" height="1" alt="" style="display:none;" />'
        if '</body>' in rendered_html.lower():
            pos = rendered_html.lower().rfind('</body>')
            rendered_html = rendered_html[:pos] + pixel_tag + rendered_html[pos:]
        else:
            rendered_html += pixel_tag
            
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
        out_dir = "dry_run_emails"
        os.makedirs(out_dir, exist_ok=True)
        safe_email = target_email.replace('@', '_at_')
        filename = f"{out_dir}/{safe_email}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Create a visible header for the simulated email
            header_html = f"""
<div style="font-family: sans-serif; background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin-bottom: 20px; border-radius: 4px;">
    <div style="margin-bottom: 5px;"><strong>From:</strong> {sender_email}</div>
    <div style="margin-bottom: 5px;"><strong>To:</strong> {target_email}</div>
    <div style="margin-bottom: 5px;"><strong>Subject:</strong> {subject}</div>
</div>
<hr>
"""
            f.write(header_html)
            f.write(html_content)
            
        print("\n" + "="*50)
        print("DRY RUN MODE - NO SMTP CREDENTIALS CONFIGURED")
        print(f"Email HTML saved for previewing to: {filename}")
        print(f"You can open this file in your browser to view the email and click the links.")
        print("-" * 50)
        print(html_content)
        print("="*50 + "\n")
        return True
