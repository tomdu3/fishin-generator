from app import app
from models import db, Template

with app.app_context():
    templates = Template.query.all()
    for t in templates:
        print(f"ID: {t.id}, Name: {t.name}")
        if '<html>' in t.body_html.lower():
            print("  Contains <html>")
        if '<body>' in t.body_html.lower():
            print("  Contains <body>")
        if '{{ tracking_url }}' not in t.body_html:
            print("  MISSING {{ tracking_url }}")
