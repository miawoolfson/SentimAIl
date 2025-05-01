import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content('This is a test email.')
msg['Subject'] = 'Test Email'
msg['From'] = 'testuser@sentimail.local'
msg['To'] = 'gal@sentimail.local'

# Connect to your Postfix SMTP server (no SSL, port 25)
with smtplib.SMTP('localhost', 25) as server:
    # Uncomment if you need to start TLS
    # server.starttls()
    
    # Login if Postfix requires auth (probably not in your case)
    # server.login('testuser', 'password')

    server.send_message(msg)

print("📨 Mail sent!")
