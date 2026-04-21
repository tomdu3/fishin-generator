# Phase 1: Initial Implementation

## Tasks Completed

- [x] 1. Setup virtual environment and install dependencies (`flask`, `flask-sqlalchemy`, `python-dotenv`).
- [x] 2. Create database models (`Target`, `Template`, `Campaign`, `TrackingEvent`) in `models.py`.
- [x] 3. Pre-seed the database with the 12 provided phishing templates.
- [x] 4. Build the core Flask app (`app.py`) and basic routing.
- [x] 5. Implement mail generation logic in `mailer.py` (tracking pixel & link rewriting).
- [x] 6. Build tracking endpoints (`/track/open/...` and `/track/click/...`).
- [x] 7. Build frontend templates (`base.html`, `dashboard.html`, `phished.html`) using Tailwind CSS.
- [x] 8. Verify the full flow (create campaign -> send -> open email -> click link -> view stats).

---

## Walkthrough

The Phishing Email Simulator has been fully built out according to the project plan. It includes a sleek dashboard for managing campaigns, a database seeded with realistic phishing templates, and a tracking system to measure engagement.

### Features Implemented

- **Modern Dashboard UI**: Built with Tailwind CSS, the dashboard provides a high-level view of campaigns and targets, designed to look like a professional business solution.
- **Pre-loaded Templates**: The database is seeded with the 12 specific templates you provided, complete with compelling, scenario-driven subjects and realistic HTML layouts.
- **Engagement Tracking**:
  - **Pixel Tracking**: An invisible 1x1 GIF is appended to each email. When the email is viewed (and images are loaded), it pings our `/track/open/` endpoint to record an "Opened" event.
  - **Link Tracking**: All links in the templates use `{{ tracking_url }}`, which dynamically inserts a unique tracking link pointing to our `/track/click/` endpoint. Clicking records the event and redirects the user to the training page.
- **Educational Landing Page**: If a user clicks a malicious link, they are directed to the "Oops! This was a Phishing Test" page, which provides immediate, constructive feedback on how they could have spotted the phishing attempt.
- **Dry-Run Email System**: By default, if no SMTP credentials are provided, the simulator outputs the generated emails directly to the terminal, allowing you to test the entire flow safely without spamming anyone.

### How to Test

1. **Start the Server**: 
   ```bash
   uv run python app.py
   ```
2. **Access the Dashboard**: Open `http://localhost:5000` in your browser.
3. **Add a Target**: Navigate to the "Targets" tab and add yourself (or a dummy user).
4. **Launch a Campaign**: Go to "New Campaign", select one of the 12 templates, select your target, and hit "Launch".
5. **View the Email (Dry Run)**: Check your terminal output. You will see the rendered HTML email output, complete with the unique tracking links.
6. **Simulate a Click**: Copy the `http://127.0.0.1:5000/track/click/...` link from the terminal output and open it in your browser. You will see the educational landing page.
7. **Check Stats**: Go back to the dashboard and view the campaign details to see the tracking events (Sent, Clicked) update in real-time.

> [!TIP]
> **Sending Real Emails**: To send actual emails, create a `.env` file in the project root with your SMTP details:
> ```env
> SMTP_SERVER=smtp.example.com
> SMTP_PORT=587
> SMTP_USER=your_username
> SMTP_PASS=your_password
> SENDER_EMAIL=security@yourcompany.com
> ```

### Project Changes
- Added Flask and SQLAlchemy dependencies to `pyproject.toml`.
- Built `models.py` defining the SQLite database schema.
- Built `app.py` as the main server and routing controller.
- Built `mailer.py` to handle the generation and dispatch of emails.
- Created the full UI suite in `templates/` utilizing Tailwind CSS.
- Implemented `seed.py` which populated the database with your 12 provided templates.
