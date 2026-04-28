from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import uuid

db = SQLAlchemy()

class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body_html = db.Column(db.Text, nullable=False)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='Draft') # Draft, Active, Completed

    template = db.relationship('Template', backref=db.backref('campaigns', lazy=True))

    @property
    def sent_count(self):
        return sum(1 for e in self.tracking_events if e.event_type == 'Sent')

    @property
    def open_count(self):
        return sum(1 for e in self.tracking_events if e.event_type == 'Opened')

    @property
    def click_count(self):
        return sum(1 for e in self.tracking_events if e.event_type == 'Clicked')

class TrackingEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('target.id'), nullable=False)
    tracking_id = db.Column(db.String(36), index=True, default=lambda: str(uuid.uuid4()))
    event_type = db.Column(db.String(20), nullable=False) # Sent, Opened, Clicked
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    campaign = db.relationship('Campaign', backref=db.backref('tracking_events', lazy=True))
    target = db.relationship('Target', backref=db.backref('tracking_events', lazy=True))
