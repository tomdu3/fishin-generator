import os
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, send_file
from models import db, Target, Template, Campaign, TrackingEvent
from dotenv import load_dotenv
from mailer import generate_email_content, send_phishing_email
from io import BytesIO

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///phishing.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def dashboard():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    targets_count = Target.query.count()
    return render_template('dashboard.html', campaigns=campaigns, targets_count=targets_count)

@app.route('/targets', methods=['GET', 'POST'])
def manage_targets():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if name and email:
            if not Target.query.filter_by(email=email).first():
                new_target = Target(name=name, email=email)
                db.session.add(new_target)
                db.session.commit()
    targets = Target.query.all()
    return render_template('targets.html', targets=targets)

@app.route('/targets/delete/<int:id>', methods=['POST'])
def delete_target(id):
    target = Target.query.get_or_404(id)
    # Be careful with cascades, but for simplicity here we just delete it
    db.session.delete(target)
    db.session.commit()
    return redirect(url_for('manage_targets'))

@app.route('/templates')
def view_templates():
    templates = Template.query.all()
    return render_template('templates.html', templates=templates)

@app.route('/campaigns/new', methods=['GET', 'POST'])
def new_campaign():
    if request.method == 'POST':
        name = request.form.get('name')
        template_id = request.form.get('template_id')
        target_ids = request.form.getlist('target_ids')

        if name and template_id and target_ids:
            campaign = Campaign(name=name, template_id=template_id, status='Active')
            db.session.add(campaign)
            db.session.commit()

            template = Template.query.get(template_id)
            
            for t_id in target_ids:
                target = Target.query.get(t_id)
                if target:
                    # Create tracking event (Sent)
                    event = TrackingEvent(campaign_id=campaign.id, target_id=target.id, event_type='Sent')
                    db.session.add(event)
                    db.session.commit() # Commit to get tracking_id generated

                    tracking_url = url_for('track_click', tracking_id=event.tracking_id, _external=True)
                    tracking_pixel_url = url_for('track_open', tracking_id=event.tracking_id, _external=True)

                    html_content = generate_email_content(template.body_html, tracking_url, tracking_pixel_url)
                    
                    # For simulating realism, we replace template variables with actual target name
                    # Note: we are just sending the rendered template, any [Service Name] etc could be parameterized in a real system.
                    send_phishing_email(target.email, template.subject, html_content)
                    
            return redirect(url_for('dashboard'))

    templates = Template.query.all()
    targets = Target.query.all()
    return render_template('campaign_new.html', templates=templates, targets=targets)

@app.route('/campaigns/<int:id>')
def campaign_details(id):
    campaign = Campaign.query.get_or_404(id)
    events = TrackingEvent.query.filter_by(campaign_id=id).order_by(TrackingEvent.timestamp.desc()).all()
    
    # Calculate stats
    sent = sum(1 for e in events if e.event_type == 'Sent')
    opens = sum(1 for e in events if e.event_type == 'Opened')
    clicks = sum(1 for e in events if e.event_type == 'Clicked')
    
    return render_template('campaign_details.html', campaign=campaign, events=events, sent=sent, opens=opens, clicks=clicks)

@app.route('/track/open/<tracking_id>.gif')
def track_open(tracking_id):
    # Transparent 1x1 GIF
    pixel_data = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    
    event = TrackingEvent.query.filter_by(tracking_id=tracking_id, event_type='Sent').first()
    if event:
        # Check if we already logged an open to prevent duplicates? For simplicity, we just log another event or update. Let's just create a new 'Opened' event.
        open_event = TrackingEvent(campaign_id=event.campaign_id, target_id=event.target_id, tracking_id=tracking_id, event_type='Opened')
        db.session.add(open_event)
        db.session.commit()
        
    return send_file(BytesIO(pixel_data), mimetype='image/gif')

@app.route('/track/click/<tracking_id>')
def track_click(tracking_id):
    event = TrackingEvent.query.filter_by(tracking_id=tracking_id).first()
    if event:
        click_event = TrackingEvent(campaign_id=event.campaign_id, target_id=event.target_id, tracking_id=tracking_id, event_type='Clicked')
        db.session.add(click_event)
        db.session.commit()
        
    return render_template('phished.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
