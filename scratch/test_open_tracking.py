from app import app, db
from models import TrackingEvent
import uuid

with app.app_context():
    # Create a dummy Sent event
    tracking_id = str(uuid.uuid4())
    sent_event = TrackingEvent(campaign_id=1, target_id=1, tracking_id=tracking_id, event_type='Sent')
    db.session.add(sent_event)
    db.session.commit()
    print(f"Created Sent event with tracking_id: {tracking_id}")

    # Simulate hitting the track_open route
    with app.test_client() as client:
        response = client.get(f'/track/open/{tracking_id}.gif')
        print(f"Response status: {response.status_code}")
        print(f"Response mimetype: {response.mimetype}")

    # Check if Opened event was created
    opened_event = TrackingEvent.query.filter_by(tracking_id=tracking_id, event_type='Opened').first()
    if opened_event:
        print("SUCCESS: Opened event created!")
    else:
        print("FAILURE: Opened event NOT created.")
