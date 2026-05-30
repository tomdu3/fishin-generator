# 📧 Email Sender Display Name Configuration & Anti-Spoofing Defenses

This document outlines how display names in email headers work, how to configure them in your local phishing simulator, and the technical defense mechanisms (SPF, DKIM, DMARC) designed to prevent and detect unauthorized sender manipulation.

---

## 🛠️ Step-by-Step Solution

### 1. How Email Display Names Work (RFC 5322)
Under **RFC 5322 (Internet Message Format)**, the `From` header can be defined in two ways:
* **Address-only format:** `user@example.com`
* **Name-addr format:** `Display Name <user@example.com>`

When a mailbox provider (such as Gmail, Outlook, or Apple Mail) displays the message, it generally displays the friendly `Display Name` in the inbox user interface, rather than the raw address. 

### 2. Dynamic Template-Level Implementation
To simulate realistic phishing campaigns, different templates need to mimic different departments or organizations. We implemented template-specific display names:

1. **Database Schema:** Added `sender_name` column to the `Template` table in [`models.py`](file:///home/tom/projects/fishin-generator/models.py).
2. **Database Seeding:** Configured realistic sender names (e.g., `"Barclays Bank Security"`, `"Zoom Support"`, `"Human Resources"`) for each entry in the seeder.
3. **Application logic:**
   - [`.env`](file:///home/tom/projects/fishin-generator/.env) is kept clean and only specifies the base sending address (e.g., `SENDER_EMAIL=tomdcoding@gmail.com`).
   - [`app.py`](file:///home/tom/projects/fishin-generator/app.py) retrieves `template.sender_name` and passes it to the mail dispatch function.
   - [`mailer.py`](file:///home/tom/projects/fishin-generator/mailer.py) dynamically constructs the `From` header using `email.utils.formataddr((sender_name, sender_address))`.

### 3. Parsing logic (Dry Run Mode)
The dry run renderer in `mailer.py` parses the generated `From` header containing the display name to display a realistic header:
```python
# Parse the combined From header to extract friendly name and raw address
name, addr = email.utils.parseaddr(from_header)
if name:
    display_from = f"{name} &lt;{addr}&gt;"
    hover_text = f"Actual Sender Address: {addr}"
else:
    display_from = addr
    hover_text = addr
```

---

## 🛡️ Email Authentication & Defensive Mechanisms

While configuring a friendly name format is standard for legitimate marketing and transactional emails, mail transfer agents (MTAs) and email clients enforce strict policies to prevent attackers from impersonating external domains.

### 1. SPF (Sender Policy Framework) - RFC 7208
* **What it does:** SPF allows domain owners to publish a DNS TXT record listing the specific IP addresses authorized to send emails on behalf of their domain.
* **Mechanism:** The receiving mail server checks the domain found in the **envelope sender** (specifically the `Return-Path` header / `MAIL FROM` command) and verifies if the sending server's IP address matches the records published in that domain's DNS.
* **Limitations:** SPF only validates the envelope sender, not the user-visible `From` header.

### 2. DKIM (DomainKeys Identified Mail) - RFC 6376
* **What it does:** DKIM provides a way to validate a domain name identity that is associated with a message through cryptographic authentication.
* **Mechanism:** The sending MTA signs the email headers and body with a private key. The public key is published in the sender domain's DNS TXT record. The receiving server fetches the public key to verify the cryptographic signature and ensure the email was not modified in transit.
* **Limitations:** Like SPF, DKIM verifies that the signature domain is valid, but does not inherently force that domain to match the user-visible `From` header.

### 3. DMARC (Domain-based Message Authentication, Reporting, and Conformance) - RFC 7489
* **What it does:** DMARC bridges the gap between SPF/DKIM validation and the user-visible `From` header to prevent spoofing.
* **Mechanism:** DMARC requires **Alignment**. This means the domain in the visible `From` header must match (or align with) either:
  * The domain verified by SPF (`Return-Path` matching `From`), or
  * The domain verified by DKIM (the `d=` tag in the DKIM-Signature header matching `From`).
* **Policy Enforcement:** If both alignments fail, DMARC instructs the receiving server on how to handle the message based on the sender's policy:
  * `p=none`: Monitor only (deliver the email).
  * `p=quarantine`: Send to Spam/Junk folder.
  * `p=reject`: Block the email entirely at the gateway level.

### 4. Client-Side Protective Features
Modern email providers implement additional user-interface mitigations:
* **External Badges:** Tagging incoming emails from outside the organization with a visible `[External]` label.
* **Unverified Sender Warnings:** Displaying warning banners if SPF/DKIM/DMARC checks fail or if the display name attempts to mimic a common corporate contact while originating from a public email address.

---

## 🌐 Official Specifications & Defensive Resources

For further technical reading on email security architecture and standards:

* **M3AAWG Email Security Best Practices:** [m3aawg.org/documents](https://www.m3aawg.org/activities/published-documents) — Best practices for senders and receivers.
* **RFC 7489 (DMARC Specification):** [datatracker.ietf.org/doc/html/rfc7489](https://datatracker.ietf.org/doc/html/rfc7489)
* **RFC 7208 (SPF Specification):** [datatracker.ietf.org/doc/html/rfc7208](https://datatracker.ietf.org/doc/html/rfc7208)
* **RFC 6376 (DKIM Specification):** [datatracker.ietf.org/doc/html/rfc6376](https://datatracker.ietf.org/doc/html/rfc6376)
* **Google Email Sender Guidelines:** [support.google.com/a/answer/81126](https://support.google.com/a/answer/81126) — Requirements for sending mail to Gmail accounts.
