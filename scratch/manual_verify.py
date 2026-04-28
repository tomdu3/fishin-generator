from app import app, db
from models import Target, Template, Campaign, TrackingEvent
from mailer import generate_email_content

with app.app_context():
    # Get a target and a template
    target = Target.query.first()
    template = Template.query.first()
    
    if not target or not template:
        print("Missing target or template. Seed the DB first.")
        exit(1)
        
    print(f"Using Target: {target.email}, Template: {template.name}")
    
    # Simulate the process in app.py:new_campaign
    campaign = Campaign(name="Verification Campaign", template_id=template.id, status='Active')
    db.session.add(campaign)
    db.session.commit()
    
    event = TrackingEvent(campaign_id=campaign.id, target_id=target.id, event_type='Sent')
    db.session.add(event)
    db.session.commit()
    
    from flask import url_for
    with app.test_request_context():
        tracking_url = url_for('track_click', tracking_id=event.tracking_id, _external=True)
        tracking_pixel_url = url_for('track_open', tracking_id=event.tracking_id, _external=True)
        
        html_content = generate_email_content(template.body_html, tracking_url, tracking_pixel_url)
        
        # Check if the dry run file was created (send_phishing_email is called in app.py)
        # Here we just check the content
        print("\nGenerated HTML Snippet:")
        print(html_content[-200:])
        
        if tracking_pixel_url in html_content:
            print("\nSUCCESS: Tracking pixel found in generated email!")
        else:
            print("\nFAILURE: Tracking pixel NOT found in generated email.")
