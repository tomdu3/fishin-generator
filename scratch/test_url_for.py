from flask import Flask, url_for

app = Flask(__name__)

@app.route('/track/open/<tracking_id>.gif')
def track_open(tracking_id):
    return tracking_id

with app.test_request_context():
    print(f"URL: {url_for('track_open', tracking_id='my-uuid')}")
