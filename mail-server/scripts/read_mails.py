import imaplib
import email
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime, formatdate  # RFC date parser
import csv
import psycopg2
import os
import requests


HOST = 'localhost'
PORT = 143  # IMAP port
# Admin credentials for IMAP proxy authentication: when logging in to a user's mailbox, use "<user>*<ADMIN_USER>" with this admin account
ADMIN_USER = 'admin@sentimail.local'
ADMIN_PASS = 'adminpass'


def get_sentiment_tag(msg_body):
    try:
        response = requests.post(
            "http://localhost:5050/sentiment",
            json={"text": msg_body},
            headers={"Content-Type": "application/json"},
            timeout=3
        )
        response.raise_for_status()
        sentiment = response.json().get("sentiment")
        if sentiment is None:
            raise ValueError("Sentiment API returned no sentiment value")
        return sentiment
    except requests.exceptions.Timeout:
        raise RuntimeError("Sentiment API request timed out - service may be down")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Sentiment API request failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error in sentiment analysis: {str(e)}")


def get_subject_tag(msg_body):
    try:
        response = requests.post(
            "http://localhost:5050/subject",
            json={"text": msg_body},
            headers={"Content-Type": "application/json"},
            timeout=3
        )
        response.raise_for_status()
        subject = response.json().get("subject")
        if subject is None:
            raise ValueError("Subject API returned no subject value")
        return subject
    except requests.exceptions.Timeout:
        raise RuntimeError("Subject API request timed out - service may be down")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Subject API request failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error in subject analysis: {str(e)}")


def print_mail(msg):
    # Print only the new mails
        print("--------------------------------")
        print("From:", msg["From"])
        print("To:", msg["To"])
        print("Subject:", msg["Subject"])
        print("Date:", msg["Date"])
        print("Message ID:", msg["Message-ID"])
        print("Sentiment Tag:", get_sentiment_tag(msg["Body"]))
        print("Subject Tag:", get_subject_tag(msg["Body"]))
        print("Body:", get_body(msg))
        print("--------------------------------")


def get_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors='replace')
                    break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode(errors='replace')
    return body


# Utility to compute how long ago the message was sent
def time_since(dt):
    """Return a timedelta representing the difference between now and dt."""
    return datetime.now(dt.tzinfo) - dt


# Utility to load all user email addresses from Dovecot's users file
def get_all_users(user_file='./scripts/mails.txt'):
    """Parse the Dovecot users file and return a list of email addresses."""
    users = []
    with open(user_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # each entry is 'email:...'
            email_addr = line.split(':', 1)[0]
            users.append(email_addr)
    return users


def get_recent_mails(mail):
    typ, data = mail.search(None, 'ALL')  # fetch all messages
    for num in data[0].split():
        # Fetch and parse each message
        typ, msg_data = mail.fetch(num, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Safely parse Date header
        date_header = msg.get("Date")
        if not date_header:
            continue
        try:
            dt = parsedate_to_datetime(date_header)
        except Exception:
            continue
        # Compute how long ago the mail was sent
        delta = time_since(dt)
        # Skip mails older than 2 minutes
        if delta > timedelta(minutes=10):
            continue

        print_mail(msg)
        add_mail_to_db(msg)


def add_mail_to_db(msg):
    DB_CONFIG = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': os.environ.get('DB_PASSWORD', ''),  # Get password from environment variable
        'host': 'localhost',
        'port': 5432  # Default PostgreSQL port
    }
    conn = None
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Insert the email data
        cur.execute("""
            INSERT INTO emails (sender, recipient, sent_at, subject, body, sentiment_tag, subject_tag)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            msg['From'],
            msg['To'],
            msg['Date'],
            msg['Subject'],
            get_body(msg),
            get_sentiment_tag(get_body(msg)),
            get_subject_tag(get_body(msg))
        ))

        conn.commit()
        print("Email inserted successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        if conn:
            cur.close()
            conn.close()


def main():
    try:
        users = get_all_users()
        for user in users:
            mail = imaplib.IMAP4(HOST, PORT)
            mail.login(f"{user}*{ADMIN_USER}", ADMIN_PASS)
            mail.select('INBOX')
            get_recent_mails(mail)
            mail.logout()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        raise  # Re-raise the exception to stop the script


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Script stopped due to error: {str(e)}")
        exit(1)  # Exit with error code 1