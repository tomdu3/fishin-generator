from app import app, db
from models import TrackingEvent

with app.app_context():
    event = TrackingEvent(campaign_id=1, target_id=1, event_type='Sent')
    db.session.add(event)
    print(f"Before commit: {event.tracking_id}")
    db.session.commit()
    print(f"After commit: {event.tracking_id}")
