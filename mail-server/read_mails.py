# import imaplib
# import email
# import os


# MAIL_SERVER = 'localhost'
# MAIL_PORT = 143
# ADMIN_USER = 'admin@sentimail.local'
# ADMIN_PASS = 'adminpass'


# def list_users(maildir_base='/var/mail'):
#     print(f"Checking directory: {maildir_base}")
#     if not os.path.exists(maildir_base):
#         print(f"Directory {maildir_base} does not exist!")
#         return []
        
#     print("Directory contents:")
#     for item in os.listdir(maildir_base):
#         full_path = os.path.join(maildir_base, item)
#         print(f"- {item} ({'directory' if os.path.isdir(full_path) else 'file'})")
        
#     users = []
#     for user in os.listdir(maildir_base):
#         if os.path.isdir(os.path.join(maildir_base, user)):
#             users.append(f"{user}@sentimail.local")
#     return users


# def fetch_emails_for_user(user_email):
#     imap = imaplib.IMAP4(MAIL_SERVER, MAIL_PORT)
#     proxy_login = f"{user_email}*{ADMIN_USER}"
    
#     imap.login(proxy_login, ADMIN_PASS)
#     imap.select('INBOX')  # or another folder
    
#     _, messages = imap.search(None, "ALL")
#     if not messages[0]:
#         print(f"No messages found for {user_email}")
#         return
        
#     for num in messages[0].split():
#         _, data = imap.fetch(num, "(RFC822)")
#         if not data or not data[0]:
#             continue
#         msg = email.message_from_bytes(data[0][1])
#         print(f"📨 Email for {user_email}")
#         print("Subject:", msg["subject"])
#         print("From:", msg["from"])
#         print("Date:", msg["date"])
#         print("---")

#     imap.logout()

# if __name__ == "__main__":
#     users = list_users('/var/mail')
#     print("\nFound users:", users)
#     for user_email in users:
#         try:
#             fetch_emails_for_user(user_email)
#         except Exception as e:
#             print(f"❌ Error fetching mails for {user_email}: {e}")

# 222222222

# from imapclient import IMAPClient

# HOST = 'localhost'
# PORT = 143  # IMAP port
# USERNAME = 'testuser@sentimail.local'
# PASSWORD = 'testpass'

# # Create connection (like psycopg2.connect)
# with IMAPClient(HOST, port=PORT, use_uid=True, ssl=False) as server:
#     server.login(USERNAME, PASSWORD)
#     server.select_folder('INBOX')

#     # Start IDLE (real-time mode)
#     server.idle()
#     print("🟢 Waiting for new emails (IDLE started)...")

#     # Check for new mail
#     while True:
#         responses = server.idle_check(timeout=60)  # returns immediately if new email
#         if responses:
#             print("📬 New mail event detected!")
#             # You can fetch the new mail here

# 333333
# import asyncio
# from aioimaplib import aioimaplib
# import email

# HOST = 'localhost'
# ADMIN_USER = 'admin@sentimail.local'
# ADMIN_PASS = 'adminpass'

# async def fetch_user_mails(user_email):
#     client = aioimaplib.IMAP4(host=HOST, port=143)
#     await client.wait_hello_from_server()
#     await client.login(f'{user_email}*{ADMIN_USER}', ADMIN_PASS)
#     await client.select('INBOX')

#     status, data = await client.search('ALL')
#     if not data or not data[0]:
#         print(f"⚠️ No messages found for {user_email}")
#         await client.logout()
#         return

#     # Convert the search results to a list of message numbers
#     message_numbers = data[0].split()
#     if not message_numbers:
#         print(f"⚠️ No valid message numbers found for {user_email}")
#         await client.logout()
#         return

#     print(f"Found {len(message_numbers)} messages for {user_email}")
    
#     for num in message_numbers:
#         try:
#             # Convert the message number to a string and ensure it's valid
#             msg_num = num.decode('utf-8')
#             if not msg_num.isdigit():
#                 print(f"⚠️ Invalid message number: {msg_num}")
#                 continue

#             # First, get the message headers to check if it's a valid message
#             status, headers = await client.fetch(msg_num, '(BODY.PEEK[HEADER])')
#             if status != 'OK' or not headers:
#                 print(f"⚠️ Failed to fetch headers for message {msg_num}")
#                 continue

#             # Now get the full message
#             status, msg_data = await client.fetch(msg_num, '(RFC822)')
#             if status != 'OK':
#                 print(f"⚠️ Failed to fetch message {msg_num}: {msg_data}")
#                 continue

#             if not msg_data or not isinstance(msg_data, list) or len(msg_data) < 1:
#                 print(f"⚠️ No message data received for message {msg_num}")
#                 continue

#             # Get the raw message data
#             raw_msg = msg_data[0][1] if isinstance(msg_data[0], tuple) else msg_data[0]
            
#             if not isinstance(raw_msg, bytes):
#                 print(f"⚠️ Message data is not bytes for message {msg_num}: {type(raw_msg)}")
#                 continue

#             msg = email.message_from_bytes(raw_msg)
            
#             # Print message details
#             print(f"📨 New email for {user_email}")
#             print(f"Message number: {msg_num}")
#             print("Subject:", msg.get('subject', 'No subject'))
#             print("From:", msg.get('from', 'No sender'))
#             print("To:", msg.get('to', 'No recipient'))
#             print("Date:", msg.get('date', 'No date'))
#             print("raw_msg:", raw_msg)
#             print(msg)
            
#             # Print message body if it exists
#             if msg.is_multipart():
#                 for part in msg.walk():
#                     if part.get_content_type() == "text/plain":
#                         try:
#                             body = part.get_payload(decode=True).decode()
#                             print("Body:", body[:100] + "..." if len(body) > 100 else body)
#                         except:
#                             print("Body: [Could not decode body]")
#             else:
#                 try:
#                     body = msg.get_payload(decode=True).decode()
#                     print("Body:", body[:100] + "..." if len(body) > 100 else body)
#                 except:
#                     print("Body: [Could not decode body]")
#             print("---")
#         except Exception as e:
#             print(f"❌ Error processing message {num} for {user_email}: {str(e)}")
#             continue

#     await client.logout()

# async def main():
#     users = ['gal@sentimail.local', 'testuser@sentimail.local']
#     await asyncio.gather(*(fetch_user_mails(user) for user in users))

# asyncio.run(main())


## 44444
import imaplib
import email

HOST = 'localhost'
PORT = 143  # IMAP port
USERNAME = 'testuser@sentimail.local'
PASSWORD = 'testpass'

mail = imaplib.IMAP4(HOST, PORT)
mail.login(USERNAME, PASSWORD)
mail.select('INBOX')

typ, data = mail.search(None, 'RECENT')  # fetch all messages
for num in data[0].split():
    typ, msg_data = mail.fetch(num, '(RFC822)')
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    print("From:", msg["From"])
    print("Subject:", msg["Subject"])
    print("Date:", msg["Date"])

    # Get body
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
    print("---")
