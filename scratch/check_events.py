from app import app
from models import TrackingEvent

with app.app_context():
    events = TrackingEvent.query.all()
    for e in events:
        print(f"ID: {e.id}, TrackingID: {e.tracking_id}, Type: {e.event_type}")
