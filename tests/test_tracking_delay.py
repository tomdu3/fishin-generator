import unittest
from unittest.mock import patch

from app import app, db, Campaign, Target, Template, TrackingEvent


class TrackingDelayTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_track_open_applies_delay_before_recording_open(self):
        template = Template(name='Test Template', subject='Test', body_html='<p>Hi</p>')
        target = Target(name='Test Target', email='target@example.com')
        campaign = Campaign(name='Test Campaign', template=template, status='Active')
        db.session.add_all([template, target, campaign])
        db.session.commit()

        sent_event = TrackingEvent(campaign_id=campaign.id, target_id=target.id, event_type='Sent')
        db.session.add(sent_event)
        db.session.commit()

        with patch('app.time.sleep') as sleep_mock:
            response = self.client.get(f'/track/open/{sent_event.tracking_id}.gif')

        self.assertEqual(response.status_code, 200)
        sleep_mock.assert_called_once_with(1)
        self.assertEqual(TrackingEvent.query.filter_by(event_type='Opened').count(), 1)


if __name__ == '__main__':
    unittest.main()
