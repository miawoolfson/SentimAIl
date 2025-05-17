import csv
import smtplib
import time
import uuid
import imaplib
from email.message import EmailMessage
from email.utils import formatdate

# Admin credentials (used for proxy login)
IMAP_HOST = 'localhost'
IMAP_PORT = 143
# Admin credentials for IMAP proxy authentication: when logging in to a user's mailbox, use "<user>*<ADMIN_USER>" with this admin account
ADMIN_USER = 'admin@sentimail.local'
ADMIN_PASS = 'adminpass'

def save_to_sent_folder(sender_email, msg):
    """Use IMAP proxy auth to save the sent message to the user's Sent folder."""
    try:
        # Proxy auth format: user*admin
        proxy_user = f"{sender_email}*{ADMIN_USER}"
        mail = imaplib.IMAP4(IMAP_HOST, IMAP_PORT)
        mail.login(proxy_user, ADMIN_PASS)
        mail.append('"Sent"', '', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
        mail.logout()
    except Exception as e:
        print(f"IMAP error for {sender_email}: {e}")

def send_emails_from_csv(csv_path='./mails-list.csv', smtp_host='localhost', smtp_port=25):
    """Send emails from CSV and save a copy to Sent folder using IMAP proxy auth."""
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            for row in reader:
                sender = row['From']
                recipient = row['To']
                subject = row['Subject']
                body = row['Body']

                msg = EmailMessage()
                msg.set_content(body)
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = recipient
                msg['Date'] = formatdate(localtime=True)
                msg['Message-ID'] = f"<{uuid.uuid4()}@{@sentimail.local}>"
                # Send the message
                server.send_message(msg)
                print(f"Sent email: from {sender} to {recipient} subject {subject}")

                # Save to Sent folder using admin proxy auth
                save_to_sent_folder(sender, msg)

if __name__ == "__main__":
    send_emails_from_csv()
