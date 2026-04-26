# Phishing Email Simulator Project Plan

The goal of this project is to build a realistic phishing email simulator that can be used for security awareness training. It will generate phishing emails, send them to targets (employees), and track engagement (opens and clicks) using a Python backend and SQLite database.

## Architecture & Technology Stack

- **Backend**: Flask (Python) - Lightweight, simple, and excellent for serving both the dashboard UI and handling tracking routes.
- **Database**: SQLite with Flask-SQLAlchemy - A simple file-based database to store campaigns, targets, and tracking events.
- **Frontend/Dashboard**: HTML + Jinja2 Templates, styled with Tailwind CSS (via CDN) for a clean, professional, and modern "business solution" aesthetic.
- **Email Delivery**: Standard Python `smtplib` + `email.mime` for generating and sending HTML emails.

## Important Considerations

**Email Delivery**: The application requires an SMTP server to actually send emails. For testing purposes, we can either:
1. Write the generated emails to the console/a local file.
2. Use a local mock SMTP server (like Mailhog or Python's built-in `smtpd`).
3. Connect to a real SMTP server (e.g., Gmail with App Passwords, SendGrid, Mailtrap).

*By default, the system will be implemented to require SMTP credentials in a `.env` file, but will default to a "Dry Run" mode (printing emails to the terminal) if no credentials are provided.*

## Application Structure

### Database & Models
- `models.py`:
  - `Target`: id, name, email
  - `Template`: id, name, subject, body_html (contains the phishing content)
  - `Campaign`: id, name, template_id, created_at, status (Draft, Active, Completed)
  - `TrackingEvent`: id, campaign_id, target_id, tracking_id (UUID), event_type (Sent, Opened, Clicked), timestamp.

### Backend Application
- `app.py`: The main Flask application. It will contain routes for:
  - **Dashboard UI**:
    - `/`: Overview of active campaigns and stats.
    - `/targets`: Manage targets (add/delete).
    - `/templates`: Manage email templates.
    - `/campaigns/new`: Create and launch a new campaign.
    - `/campaigns/<id>`: View campaign results (opens, clicks).
  - **Tracking Routes**:
    - `/track/open/<tracking_id>.gif`: Serves a 1x1 transparent pixel and records an "Opened" event.
    - `/track/click/<tracking_id>`: Records a "Clicked" event and redirects the user to an educational "Oops, this was a phishing test!" page.

- `mailer.py`: Contains the logic for sending emails, embedding the tracking pixel, and rewriting links in the email template to pass through our `/track/click/` route.

### Frontend Templates
- `templates/base.html`: Base layout using Tailwind CSS.
- `templates/dashboard.html`: Overview of campaigns and metrics.
- `templates/phished.html`: The "You've been phished" landing page that employees see when they click a malicious link. It explains how they were tricked (social engineering training).

## Next Steps
1. Setup virtual environment and dependencies.
2. Initialize Flask and database models.
3. Build the core dashboard views and templates.
4. Implement the mail generation and sending logic.
5. Implement the tracking endpoints.
