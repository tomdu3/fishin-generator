# Fishin' Generator

![Fishin' Generator](./docs/project.png)

Fishin' Generator is a phishing email simulator that can be used for security awareness training. It will generate phishing emails, send them to targets (employees), and track engagement (opens and clicks) using a Python backend and SQLite database.

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with Flask-SQLAlchemy
- **Frontend**: HTML + Jinja2 Templates, styled with Tailwind CSS (via CDN)

## How to Run

1. Ensure you have [uv](https://docs.astral.sh/uv/) installed.
2. Install the dependencies:
   ```bash
   uv sync
   ```
3. Run the Flask application:
   ```bash
   uv run app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`
