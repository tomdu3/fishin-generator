# 🛠️ Troubleshooting Local Testing & Tracking Issues

When running this phishing simulator locally (`http://localhost:5000` or `http://127.0.0.1:5000`), you will encounter issues when trying to track **Opens** and **Clicks** from actual email clients. 

This document explains why this happens and provides step-by-step instructions on how to resolve it.

---

## 🔍 The Issues

### 1. "Opened" Events (Pixels) Do Not Track in Webmail (e.g., Gmail, Outlook.com)
Modern webmail clients use **image proxy servers** (such as the Google Image Proxy) to fetch and cache images. When an email is received, Google's servers attempt to download the `1x1` tracking pixel. Since `http://127.0.0.1:5000` is only accessible on *your* local machine, Google's servers cannot reach it, causing the tracking request to fail.

### 2. "Clicked" Events Do Not Work on Mobile or External Devices
If you open a simulation email on your phone, clicking a link pointing to `http://127.0.0.1:5000` will fail. Your phone will look for the server on its own local loopback address (`127.0.0.1`) rather than your computer.

### 3. Interstitial Warning Pages Block Tracking Pixels (Gmail/Outlook Proxy Block)
When using free tunnel providers (like **Localtunnel** or **Ngrok's Free Tier**) to expose localhost, they present an anti-abuse warning/interstitial landing page to first-time visitors.
When Gmail's background image proxy attempts to fetch your tracking pixel from the tunnel URL, it receives the HTML warning page instead of the transparent GIF. Since it cannot click through the warning, the image fails to load and **never reaches your Flask app**, preventing the "Opened" event from being recorded.

---

## 🛠️ Solutions for Local Testing

### Solution A: Use `localtunnel` (Quickest, No Signup)
Expose your local Flask server to the public internet using a secure HTTPS tunnel.

1. Ensure your Flask server is running locally:
   ```bash
   uv run app.py
   ```
2. Open a new terminal window and run:
   ```bash
   npx localtunnel --port 5000
   ```
3. Copy the public URL provided (e.g., `https://short-snakes-crawl.loca.lt`).
4. **Important**: Open your browser and navigate to that public tunnel URL.
5. Launch your campaigns from the admin interface **while accessed via the public tunnel URL**.
   - *Why?* Flask generates external tracking links dynamically using the request's hostname. Accessing it via the tunnel URL forces the generated email links to use the public HTTPS URL (e.g., `https://short-snakes-crawl.loca.lt/track/click/...`).
6. Clicks and opens will now track successfully from any email client or device.

---

### Solution B: Use `ngrok` (Highly Reliable)
Expose your local port to the internet via ngrok.

1. Download and install [ngrok](https://ngrok.com/).
2. Run your Flask app.
3. Start the ngrok tunnel on port `5000`:
   ```bash
   ngrok http 5000
   ```
4. Copy the public forwarding HTTPS URL (e.g., `https://a1b2-34-56.ngrok-free.app`).
5. Open this URL in your browser and use it to access the dashboard and send your test campaigns.

---

### Solution C: Offline Testing (Dry Run Mode)
Test the database logging and dashboard UI completely offline without configuring an email server or exposing ports.

1. Remove or rename your `.env` file to ensure no SMTP credentials are loaded.
2. Run the application:
   ```bash
   uv run app.py
   ```
3. Send a test campaign. The terminal will log that it is in **Dry Run Mode**.
4. Open the `dry_run_emails/` folder in the project root.
5. Double-click the generated `.html` file for your target. This opens the email locally in your browser.
6. Click the call-to-action link (e.g., "Reset Password"). Since you are on the same machine, the link will successfully send a request to `localhost:5000`, recording the click event on your dashboard.

---

### Solution D: Bypass Interstitial Warning Pages using Serveo or Cloudflare Tunnels (For Gmail/Outlook Apps)
To solve **Issue #3** and successfully track opens inside webmail applications like Gmail and Outlook, you need to use a tunnel provider that does **not** serve warning pages.

#### Option 1: Serveo (Built-in SSH, No Installation)
1. Ensure your Flask server is running locally.
2. Open a new terminal and run:
   ```bash
   ssh -R 80:localhost:5000 serveo.net
   ```
3. Copy the forwarding URL printed in your terminal (e.g., `https://xxxx.serveo.net`).
4. Access your dashboard using that URL, and send your test campaigns. Clicks and opens will now track perfectly in Gmail!

#### Option 2: Cloudflare Tunnels (Highly Reliable)
1. Ensure your Flask server is running.
2. Open a new terminal and run:
   ```bash
   npx @cloudflare/cloudflared tunnel --url http://localhost:5000
   ```
3. Copy the generated `.trycloudflare.com` URL (e.g., `https://your-subdomain.trycloudflare.com`).
4. Access your local dashboard using that URL and launch your campaign.
