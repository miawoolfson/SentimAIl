import imaplib
import email
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime, formatdate  # RFC date parser
import csv


HOST = 'localhost'
PORT = 143  # IMAP port
# Admin credentials for IMAP proxy authentication: when logging in to a user's mailbox, use "<user>*<ADMIN_USER>" with this admin account
ADMIN_USER = 'admin@sentimail.local'
ADMIN_PASS = 'adminpass'


def print_mail(msg):
    # Print only the new mails
        print("--------------------------------")
        print("From:", msg["From"])
        print("To:", msg["To"])
        print("Subject:", msg["Subject"])
        print("Date:", msg["Date"])
        # Get and print body
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
        print("Body:", body)
        print("--------------------------------")

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
        if delta > timedelta(minutes=5):
            continue

        print_mail(msg)

def main():
    users = get_all_users()
    for user in users:
        mail = imaplib.IMAP4(HOST, PORT)
        mail.login(f"{user}*{ADMIN_USER}", ADMIN_PASS)
        mail.select('INBOX')
        get_recent_mails(mail)
        mail.logout()

def all_mail():
    """Read and print all mails for every user in users file."""
    users = get_all_users()
    for user in users:
        mail = imaplib.IMAP4(HOST, PORT)
        mail.login(f"{user}*{ADMIN_USER}", ADMIN_PASS)
        mail.select('INBOX')
        typ, data = mail.search(None, 'ALL')
        for num in data[0].split():
            typ, msg_data = mail.fetch(num, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            print_mail(msg)
        mail.logout()



if __name__ == "__main__":
    # add_csv_mails()
    # read_csv_mails()
    # all_mail()
    main()