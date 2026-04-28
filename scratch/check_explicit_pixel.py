from app import app
from models import Template

with app.app_context():
    for t in Template.query.all():
        if 'tracking_pixel_url' in t.body_html:
            print(f"FOUND in {t.name}")
