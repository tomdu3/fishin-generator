from app import app
from models import db, Template

templates_data = [
    {
        "name": "Credential Reset Notification",
        "subject": "Action Required: Password Expiration for Barclays Bank",
        "body_html": """
        <p>Your Barclays Bank password will expire in 24 hours. To avoid disruption, reset your password now using the secure link below.</p>
        <p><a href="{{ tracking_url }}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
        """
    },
    {
        "name": "Executive Wire Transfer Request",
        "subject": "Urgent Request: Wire Transfer Needed for SpaceX Launchpad",
        "body_html": """
        <p>Please process a wire transfer of $5.2M to Elon Musk today to finalize the SpaceX Launchpad contract. I’m in meetings and can’t call—just confirm once done.</p>
        <p>Signature: Donald Trump, CEO</p>
        <p><a href="{{ tracking_url }}">Click here to view transfer details</a></p>
        """
    },
    {
        "name": "Vendor Payment Update",
        "subject": "Updated Banking Instructions for Invoice #123456",
        "body_html": """
        <p>Please note our new remittance details for Invoice #123456, due on 04/30/2026. Let us know once payment is sent.</p>
        <p><a href="{{ tracking_url }}" style="color: blue; text-decoration: underline;">Attachment: New_Bank_Details.pdf</a></p>
        """
    },
    {
        "name": "Policy Document Signature Request",
        "subject": "Please Review: Updated Data Security Policy",
        "body_html": """
        <p>All employees are required to review and sign the updated Data Security policy. Download the document, review, and sign by 05/31/2026.</p>
        <p><a href="{{ tracking_url }}" style="color: blue; text-decoration: underline;">Attachment: Data_Security_Policy_2026.docx</a></p>
        """
    },
    {
        "name": "Fake File Share Notification",
        "subject": "[External] Jeff Bezos Shared a Document with You",
        "body_html": """
        <p>Jeff Bezos has sent you a secure file via Sharepoint. Click below to access the document.</p>
        <p><a href="{{ tracking_url }}" style="display: inline-block; padding: 10px 20px; background-color: #28a745; color: #fff; text-decoration: none; border-radius: 5px;">View Document</a></p>
        """
    },
    {
        "name": "Callback Phishing Request",
        "subject": "Payment Issue: Immediate Attention Required",
        "body_html": """
        <p>We were unable to process your recent payment to Spotify Premium. Please call our billing department at (888) 777-1111 to avoid service disruption.</p>
        <p>Phone Number: (888) 777-1111</p>
        <p><a href="{{ tracking_url }}">Or click here to review the invoice online</a></p>
        """
    },
    {
        "name": "QR Code Login Verification",
        "subject": "Suspicious Login Attempt Detected—Action Required",
        "body_html": """
        <p>We detected a login attempt from an unrecognized device. Scan the QR code below to verify your identity and secure your account.</p>
        <p><em>(Simulation: Click the link below instead of a QR code)</em></p>
        <p><a href="{{ tracking_url }}">Verify Identity Now</a></p>
        """
    },
    {
        "name": "Payroll Change Request",
        "subject": "Confirm Your Direct Deposit Details",
        "body_html": """
        <p>Ahead of our upcoming payroll cycle, please confirm your direct deposit information to avoid delays. Use the secure form linked below.</p>
        <p><a href="{{ tracking_url }}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px;">Confirm Details</a></p>
        """
    },
    {
        "name": "MFA Fatigue Bypass Email",
        "subject": "Action Required: MFA System Update",
        "body_html": """
        <p>We’ve made changes to our MFA system. You may receive a verification prompt—please approve it to finalize setup.</p>
        <p><a href="{{ tracking_url }}">Click here to manually approve</a></p>
        <p>Signature: [IT Support Name], IT Security Team</p>
        """
    },
    {
        "name": "Calendar Invite from Unknown Contact",
        "subject": "[Invite] Strategy Planning Session with [Fake Host Name]",
        "body_html": """
        <p>Please review the meeting agenda in advance: <a href="{{ tracking_url }}">Meeting Agenda</a>. Let me know if you have any questions before we meet.</p>
        <p><a href="{{ tracking_url }}" style="color: blue; text-decoration: underline;">Add to Calendar: [ICS file or embedded calendar link]</a></p>
        """
    },
    {
        "name": "Software Update Prompt",
        "subject": "Required: Zoom Security Update",
        "body_html": """
        <p>Install the attached update to continue using Zoom with the latest compliance settings.</p>
        <p><a href="{{ tracking_url }}" style="color: blue; text-decoration: underline;">Attachment: Zoom_Update_Installer.pkg</a></p>
        """
    },
    {
        "name": "Fake Benefits Enrollment Notification",
        "subject": "Final Reminder: Benefits Enrollment Ends Tomorrow",
        "body_html": """
        <p>Click below to finalize your 2025 elections before the window closes.</p>
        <p><a href="{{ tracking_url }}" style="display: inline-block; padding: 10px 20px; background-color: #dc3545; color: #fff; text-decoration: none; border-radius: 5px;">Review Benefits</a></p>
        """
    }
]

def seed():
    with app.app_context():
        db.create_all()
        if Template.query.count() == 0:
            for t in templates_data:
                template = Template(name=t['name'], subject=t['subject'], body_html=t['body_html'])
                db.session.add(template)
            db.session.commit()
            print(f"Seeded {len(templates_data)} templates.")
        else:
            print("Templates already seeded.")

if __name__ == '__main__':
    seed()
