# Mail Server with Postfix, Dovecot, and Rainloop

This repository provides a fully containerized mail server using Postfix (SMTP), Dovecot (IMAP/POP3), and Rainloop (webmail interface).

## Services

### Postfix

What it is: A mail transfer agent (MTA) that sends and routes email.

Purpose:
- Accepts outgoing mail from users and delivers it to local mailboxes or remote servers.
- Processes incoming SMTP connections and enqueues messages.

In a local setup:
- Relays messages between local users via SMTP.
- Works with RainLoop webmail to send outgoing mail.

How it works:
- Listens on port 25 for SMTP.
- Receives mail from webmail apps (e.g., RainLoop).
- Delivers mail to Dovecot using LMTP or a local delivery command.

Example: If Alice sends an email to Bob using RainLoop, Postfix gets the message and sends it to Bob's mailbox.

Built from the `postfix/` directory.

### Dovecot

What it is: A Mail Delivery Agent (MDA) and IMAP/POP3 server that stores and serves emails to users.

Purpose:
- Stores mail in Maildir format for each user.
- Authenticates users and serves mail via IMAP.

In a local setup:
- Accepts mail delivered by Postfix (via LMTP).
- Provides mailbox access to users over IMAP.

How it works:
- Listens on port 143 for IMAP.
- Authenticates users against `/etc/dovecot/users`.
- Serves mail stored under `/var/mail`.
- Ensures proper Maildir structure for each mailbox.

Example: When Bob logs in to RainLoop to read his mail, Dovecot is what actually shows him his inbox.

Built from the `dovecot/` directory.

### Rainloop
Rainloop is a modern webmail client.
- Listens on port 8888.
- Provides a browser-based interface for reading and sending email.
- Stores its data in `/rainloop/data` volume.
- Uses the `hardware/rainloop` Docker image.

## Prerequisites

- Docker
- Docker Compose

## Running the Stack

1. Clone the repository:
   ```bash
   git clone https://github.com/miawoolfson/SentimAIl.git
   cd mail-server
   ```
2. Start the containers:
   ```bash
   docker-compose up -d
   ```
3. Verify the services are running:
   ```bash
   docker-compose ps
   ```
4. Access Rainloop Webmail:
   Open your browser at http://localhost:8888

## Adding Mail Users

A helper script is provided to add virtual mailbox users:

1. Edit `scripts/mails.txt`, adding lines in the format:
   ```
   user@sentimail.local:password
   ```
2. Run the script:
   ```bash
   ./scripts/add-mail-users.sh
   ```

This process:
- Adds entries to Postfix's `/etc/postfix/vmailbox` and updates the hash db.
- Adds entries to Dovecot's `/etc/dovecot/users` and sets proper ownership.
- Creates a Maildir structure under `/var/mail/<user>/Maildir`.
- Restarts the Postfix and Dovecot containers if new users were added.

## Sending mails from csv

To send emails in bulk, you can use the `scripts/send_mails.py` Python script. The script reads a CSV file containing columns `From`, `To`, `Subject`, and `Body`, sends each email via SMTP, and saves a copy in the sender's Sent folder using IMAP proxy authentication.

Example CSV format:
```csv
From,To,Subject,Body
alice@sentimail.local,bob@sentimail.local,Hello,Hi Bob, this is a test email.
user2@sentimail.local,user3@sentimail.local,Test,This is another email.
```

Usage:
```bash
python3 -m venv venv-send-mails
source venv-send-mails/bin/activate 
python3 ./scripts/send_mails.py
```
- `csv_path` (default: [`./mails-list.csv`](./mails-list.csv))

## Reading mails with the script

You can fetch and display recent mails for all virtual users using the `scripts/read_mails.py` script. It logs in to each user's INBOX via IMAP proxy, retrieves messages sent in the last 5 minutes, and prints the message headers and body.

Before running the script, set the database password as an environment variable:
```bash
export DB_PASSWORD='your_database_password'
```

Usage:
```bash
python3 -m venv venv-read-mails
source venv-read-mails/bin/activate 
pip3 install -r ./scripts/requirements.txt
python3 ./scripts/read_mails.py
```

To list all messages regardless of time, edit the script to call the `all_mail()` function instead of `main()`.

## Troubleshooting

View logs for any service:
```bash
   docker-compose logs -f postfix
   docker-compose logs -f dovecot
   docker-compose logs -f rainloop
