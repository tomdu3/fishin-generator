from app import app
from models import Template

with app.app_context():
    for t in Template.query.all():
        print(f"NAME: {t.name}")
        print(f"BODY: {t.body_html}")
        print("---")
