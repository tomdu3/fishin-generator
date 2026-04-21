# Project Overview

The goal of this project is to build an internal tool that simulates phishing attacks to evaluate and train users' cybersecurity awareness. The backend is built using Python with the Flask framework, utilizing Flask-SQLAlchemy for interacting with a local SQLite database. The frontend features a responsive, professional dashboard designed with Tailwind CSS to manage the workflow.

The core features include a central dashboard for managing "targets" (the users being tested) and launching simulated campaigns. The system is pre-seeded with twelve realistic phishing email templates ranging from fake password resets to urgent HR requests. When a campaign runs, it generates customized emails and either dispatches them via SMTP or outputs them in a safe "dry-run" mode in the terminal for testing. If a user falls for the simulation, they are directed to an educational landing page that provides immediate feedback on how to spot similar attacks in the future.

To measure engagement, the application implements two specific detection techniques:
1. **Open Tracking:** An invisible 1x1 pixel GIF is appended to the bottom of each HTML email payload. When the email client loads images, it makes a request to a `/track/open/` endpoint on the server, allowing the system to log that the email was successfully viewed.
2. **Click Tracking:** Every malicious link within the phishing templates is dynamically rewritten to point to a unique `/track/click/` endpoint. When a user clicks a link, the server registers the event against their unique tracking ID before seamlessly redirecting them to the educational landing page.

This stack and tracking methodology allows for a safe, comprehensive simulation environment.
