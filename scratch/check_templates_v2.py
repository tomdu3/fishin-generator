from app import app
from models import db, Template

with app.app_context():
    templates = Template.query.all()
    for t in templates:
        issues = []
        if '{{ tracking_url }}' not in t.body_html:
            issues.append("Missing {{ tracking_url }}")
        if '<html>' in t.body_html.lower():
            issues.append("Contains <html>")
        if '<body>' in t.body_html.lower():
            issues.append("Contains <body>")
        
        if issues:
            print(f"ID: {t.id}, Name: {t.name}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"ID: {t.id}, Name: {t.name} - OK")
