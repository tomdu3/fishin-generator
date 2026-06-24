# Deployment, Email Security, and Authentication Roadmap

This guide provides a comprehensive roadmap and step-by-step guidance to deploy the **Fishin' Generator** simulator securely. It addresses three primary concerns: selecting a suitable email sending service, preventing abuse by unauthorized users on the public internet, and securing the simulator dashboard.

Rather than providing raw code templates, this document outlines the core concepts, logical flows, and security principles needed for you to design and implement these features yourself.

---

## 📋 Table of Contents
1. [Email Service Strategy: Avoiding Bans](#1-email-service-strategy-avoiding-bans)
2. [Abuse Prevention: Securing the Outbound Mailbox](#2-abuse-prevention-securing-the-outbound-mailbox)
3. [Authentication & Authorization System](#3-authentication--authorization-system)
4. [Step-by-Step Deployment Walkthrough](#4-step-by-step-deployment-walkthrough)

---

## 1. Email Service Strategy: Avoiding Bans

Using personal email accounts (like standard Gmail) or free tiers of transactional Email Service Providers (ESPs) (such as SendGrid, Mailgun, or Resend) for phishing simulations often leads to issues.

### The Problem: Automated Compliance Scanners
Modern ESPs use automated heuristic scanners to look for suspicious content in outgoing emails (e.g., words like "password reset," "verify account," "security warning," or links pointing to domain names that mimic known brands). Because phishing simulators inherently send these types of emails, **your account will likely be suspended by the ESP's compliance team within minutes of launching your first campaign.**

### The Strategic Options

#### Option A: Local Sandbox / SMTP Traps (For Safe Learning & Local Testing)
* **How it works**: Use a service like **Mailtrap** or run a local utility like **Mailhog**. These systems act as standard SMTP servers, but instead of delivering the emails to the external internet, they capture them in a sandbox dashboard.
* **Implementation Goal**: Set your SMTP environment variables to point to the sandbox host. This allows you to verify that email headers are generated correctly and links are rewritten without sending actual emails.

#### Option B: Transactional ESPs with Domain Authentication (For Small-scale Authorized Tests)
* **How it works**: Choose a provider with a free daily quota (such as **Brevo**). 
* **Requirements**:
  * You must verify ownership of your sending domain by adding DNS records (DKIM and SPF).
  * You must ensure templates avoid referencing external brands that do not match your verified domain.
  * Keep campaign sizes small to avoid triggering automated spikes in spam reports.

#### Option C: Self-Hosted SMTP (For Professional Phishing Exercises)
* **How it works**: Configure a mail transfer agent (like Postfix or Exim) on a small Virtual Private Server (VPS) you control.
* **Requirements**:
  * Since there is no compliance scanner blocking your templates, you are responsible for mail delivery reputation.
  * You must configure DNS records manually: **SPF** (defining who can send mail), **DKIM** (signing emails cryptographically), **DMARC** (specifying policies for failures), and **PTR/Reverse DNS** (linking your IP address back to your domain).

---

## 2. Abuse Prevention: Securing the Outbound Mailbox

When you deploy this application publicly, anyone who finds your website can access the dashboard. If your app is configured with a default SMTP connection, a malicious actor could abuse it to spam others or launch real phishing attacks.

To prevent this, you should build these guardrails:

### Goal 1: Move Credentials to User Settings (Decoupled SMTP)
Instead of storing SMTP credentials globally in the server's environment variables:
1. **Database Schema**: Design a settings table or update your models to save SMTP server details (host, port, username, password) securely.
2. **Security**: Encrypt the stored password in the database using a symmetric encryption library (like `cryptography.fernet`).
3. **Controller Logic**: Modify your mail dispatch functions to query these settings and initialize the `smtplib` connection dynamically for each campaign, rather than using global environmental fallbacks.

### Goal 2: Target Domain Whitelisting
Prevent users from sending emails to arbitrary target domains.
1. **Logic**: Create a configuration list of authorized domain names (e.g., your organization's domain).
2. **Validation**: Before saving targets or scheduling a campaign, parse each recipient's email address. Extract the domain suffix (the part after `@`) and ensure it matches the whitelist.
3. **Handling Failures**: Return a descriptive validation error to the operator if they attempt to add an unauthorized email address.

### Goal 3: Application-Level Rate Limiting
Prevent automated scripts from abusing campaign execution endpoints.
1. **Library**: Research Python packages like `Flask-Limiter`.
2. **Logic**: Apply limits per IP address or per authenticated user account (e.g., maximum of 3 campaign runs per hour).
3. **Implementation**: Ensure that your rate limits return an appropriate HTTP status code (e.g., `429 Too Many Requests`) with a user-friendly warning message.

---

## 3. Authentication & Authorization System

A phishing dashboard contains targets' names, emails, and engagement metrics (PII and vulnerability data). You must protect this dashboard behind an authentication barrier.

### Step 1: Install a Session Management Library
Use a well-established framework for session handling, such as `Flask-Login`. It handles browser cookies, session lifetimes, and route protection.

### Step 2: Design the User Model
Add a `User` table to your database.
1. **Fields**: At minimum, include a primary key, a unique username string, and a password hash string.
2. **Cryptographic Hashing**: **Never store passwords in plain text.** Use secure hashing algorithms like `scrypt` or `bcrypt` via Python's standard libraries or Werkzeug (`generate_password_hash` and `check_password_hash`).

### Step 3: Implement Authentication Endpoints
Create routes to manage the user lifecycle:
1. **`/setup` (First-Time Initialization)**:
   * **Purpose**: Allow the deployment administrator to register the initial account.
   * **Security Check**: This route must check if any users exist in the database. If a user already exists, immediately redirect to `/login` to prevent an attacker from taking over a newly deployed database.
2. **`/login`**:
   * Collect credentials from a POST request.
   * Verify the hashed password against the database record.
   * On success, log the user in and redirect to the dashboard.
3. **`/logout`**:
   * Terminate the user session and clear browser session cookies.

### Step 4: Protect Existing Routes
Ensure that every route in your application (except `/login`, `/setup`, and the tracking endpoints) requires an active authenticated session.
1. **Decorator**: Use authentication decorators (such as `@login_required`) on all dashboard, templates, targets, and campaign routes.
2. **Anonymous Access**: The tracking routes (`/track/open/...` and `/track/click/...`) must remain accessible without authentication so that email clients and targets can trigger events.

---

## 4. Step-by-Step Deployment Walkthrough

To host the application online, you have several platforms available, each with different storage and scaling architectures. Here are the roadmaps for three popular cloud platforms:

### Option A: Render.com (Recommended for SQLite persistence)
Render is a container-based platform that supports persistent volume disks, making SQLite setup simple and reliable.

1. **Install Gunicorn**: Ensure `gunicorn` is listed in your project dependencies. Do not use Flask's built-in server in production.
2. **Environment Secrets**: Configure your application to read configuration values (like `SECRET_KEY` and `DATABASE_URL`) from environment variables.
3. **Mount a Disk**: In the Render dashboard, add a persistent volume disk to your web service (e.g. named `sqlite-db` mounted at `/data`).
4. **Define Connection**: Set the `DATABASE_URL` environment variable to write inside that disk directory (e.g. `sqlite:////data/phishing.db`).
5. **Start Command**: Configure the start command in your service settings to run the server with Gunicorn: `gunicorn app:app`.

### Option B: Railway.app (Excellent alternative for persistent SQLite)
Railway is also a container-based platform with robust GitHub integration and persistent disk support.

1. **Create a Service**: Create a new project on Railway and choose "Deploy from GitHub repository".
2. **Attach a Volume**:
   * Navigate to your service settings in the Railway dashboard.
   * Add a persistent storage volume (e.g., mounted at `/data`).
3. **Configure Environment Variables**:
   * Set `DATABASE_URL` to point to the volume: `sqlite:////data/phishing.db`.
   * Set `SECRET_KEY` to a secure random string.
4. **App Initialization & Port binding**:
   * Ensure your Flask startup reads the dynamic `$PORT` variable from the environment or relies on Gunicorn which binds automatically.
   * Create a `Procfile` in the root of your project or specify the start command in the Railway dashboard: `gunicorn app:app`.

### Option C: Vercel.com (Serverless - Requires external database)
Vercel hosts applications using **stateless Serverless Functions**. Because serverless instances spin up and down dynamically, any file written to a local SQLite database file will be **lost** when the function goes idle. 

If you wish to deploy to Vercel, you must adapt your architecture:

1. **External Database Required**: You must spin up an external, hosted database (e.g., a free PostgreSQL database on Supabase or Neon) and set `DATABASE_URL` to point to it.
2. **Postgres Driver**: Install a Python-compatible driver (such as `psycopg2-binary` or `pg8000`) so SQLAlchemy can talk to PostgreSQL.
3. **Vercel Configuration (`vercel.json`)**:
   * Create a `vercel.json` configuration file in the project root.
   * Configure builds to use the Vercel Python builder (`@vercel/python`) pointing to your `app.py` entrypoint.
   * Configure routes to redirect all incoming traffic to `app.py`.
4. **WSGI Handler**: Ensure the Flask instance (the `app` object) is exposed at the top level of your `app.py` so Vercel's serverless runtime can access and wrap it.

---

## 📚 Useful Resources

Here are verified documentation links, tutorials, and video guides to help you implement and deploy these security updates:

### 📧 Email Services & Authentication
* **Mailtrap Sandbox**:
  * Website: [Mailtrap](https://mailtrap.io/)
  * Documentation: [Mailtrap Email Testing Sandbox Docs](https://mailtrap.io/email-sandbox/)
* **Email Protocols (SPF, DKIM, DMARC)**:
  * Video Guide: [Email Authentication Explained: SPF, DKIM, and DMARC by Office365Concepts (YouTube)](https://www.youtube.com/watch?v=203N8aR2yXg)

### 🔒 User Authentication & Security
* **Session Management**:
  * Documentation: [Flask-Login official documentation](https://flask-login.readthedocs.io/)
* **Password Hashing**:
  * Documentation: [Werkzeug Password Hashing Utilities](https://werkzeug.palletsprojects.com/)
* **Full-Stack Tutorial Video (Highly Recommended)**:
  * Video Playlist: [Corey Schafer's Flask Web Development Series (YouTube)](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH) – Sections 5 (Databases), 6 (User Authentication), and 11 (Deployment) walk step-by-step through configuring models and Flask-Login.

### 🛡️ Abuse Prevention & Rate Limiting
* **Rate Limiting**:
  * Documentation: [Flask-Limiter official documentation](https://flask-limiter.readthedocs.io/)

### 🚀 Production Deployment & Hosting
* **Render.com**:
  * Guide: [Deploy a Flask App on Render](https://render.com/docs/deploy-flask)
  * Storage: [Render Persistent Disks Documentation](https://render.com/docs/disks)
* **Railway.app**:
  * Guide: [Railway Guides Hub](https://railway.app/guides)
* **Vercel.com**:
  * Guide: [Vercel Python Runtime Serverless Docs](https://vercel.com/docs/functions/runtimes/python)
* **Fly.io**:
  * Guide: [Python on Fly.io Documentation](https://fly.io/docs/languages-and-frameworks/python/)
