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
    if request.headers.get('HX-Request'):
        return render_template('partials/target_list.html', targets=targets)
    return render_template('targets.html', targets=targets)

@app.route('/dashboard/stats')
def dashboard_stats():
    campaigns = Campaign.query.all()
    targets_count = Target.query.count()
    return render_template('partials/dashboard_stats.html', campaigns=campaigns, targets_count=targets_count)

@app.route('/dashboard/campaigns')
def campaign_list():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return render_template('partials/campaign_list.html', campaigns=campaigns)

@app.route('/targets/delete/<int:id>', methods=['POST'])
def delete_target(id):
    target = db.get_or_404(Target, id)
    # Be careful with cascades, but for simplicity here we just delete it
    db.session.delete(target)
    db.session.commit()
    if request.headers.get('HX-Request'):
        targets = Target.query.all()
        return render_template('partials/target_list.html', targets=targets)
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

            template = db.session.get(Template, template_id)
            
            for t_id in target_ids:
                target = db.session.get(Target, t_id)
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
    campaign = db.get_or_404(Campaign, id)
    events = TrackingEvent.query.filter_by(campaign_id=id).order_by(TrackingEvent.timestamp.desc()).all()
    
    # Calculate stats
    sent = sum(1 for e in events if e.event_type == 'Sent')
    opens = sum(1 for e in events if e.event_type == 'Opened')
    clicks = sum(1 for e in events if e.event_type == 'Clicked')
    
    return render_template('campaign_details.html', campaign=campaign, events=events, sent=sent, opens=opens, clicks=clicks)

@app.route('/campaigns/<int:id>/stats')
def campaign_stats(id):
    events = TrackingEvent.query.filter_by(campaign_id=id).all()
    sent = sum(1 for e in events if e.event_type == 'Sent')
    opens = sum(1 for e in events if e.event_type == 'Opened')
    clicks = sum(1 for e in events if e.event_type == 'Clicked')
    return render_template('partials/campaign_stats.html', sent=sent, opens=opens, clicks=clicks)

@app.route('/campaigns/<int:id>/events')
def campaign_events(id):
    events = TrackingEvent.query.filter_by(campaign_id=id).order_by(TrackingEvent.timestamp.desc()).all()
    return render_template('partials/event_list.html', events=events)

@app.route('/track/open/<tracking_id>.gif')
def track_open(tracking_id):
    # Transparent 1x1 GIF
    pixel_data = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    
    # Robust lookup: find ANY event with this tracking_id to get campaign/target info
    event = TrackingEvent.query.filter_by(tracking_id=tracking_id).first()
    if event:
        open_event = TrackingEvent(
            campaign_id=event.campaign_id, 
            target_id=event.target_id, 
            tracking_id=tracking_id, 
            event_type='Opened'
        )
        db.session.add(open_event)
        db.session.commit()
        print(f"Open tracked for target {event.target_id} in campaign {event.campaign_id}")
    else:
        print(f"Open tracking failed: tracking_id {tracking_id} not found")
        
    return send_file(BytesIO(pixel_data), mimetype='image/gif')

@app.route('/track/click/<tracking_id>')
def track_click(tracking_id):
    event = TrackingEvent.query.filter_by(tracking_id=tracking_id).first()
    if event:
        click_event = TrackingEvent(
            campaign_id=event.campaign_id, 
            target_id=event.target_id, 
            tracking_id=tracking_id, 
            event_type='Clicked'
        )
        db.session.add(click_event)
        db.session.commit()
        print(f"Click tracked for target {event.target_id} in campaign {event.campaign_id}")
    else:
        print(f"Click tracking failed: tracking_id {tracking_id} not found")
        
    return render_template('phished.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
