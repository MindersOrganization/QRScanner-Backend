import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from typing import List


def send_emails(subject: str, bodies: List[str], to_emails: List[str], username: str, password: str) -> None:
    """
    Send an email using Gmail.
    :param subject: Email subject
    :param bodies: List of email bodies, one for each recipient
    :param to_emails: List of recipient email addresses
    :param username: Gmail username
    :param password: Gmail password
    """
    # Check that the number of email bodies matches the number of recipients
    if len(bodies) != len(to_emails):
        raise ValueError("The number of email bodies must match the number of recipients")

    # Create a secure SSL/TLS connection to the Gmail server
    server: smtplib.SMTP_SSL = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    # Login to the Gmail server
    server.login(username, password)

    # Set the maximum number of emails that can be sent in a day for a free Gmail account
    max_emails_per_day: int = 500

    # Keep track of the number of emails sent in a day
    emails_sent: int = 0

    # For each recipient, send the email
    for body, to_email in zip(bodies, to_emails):
        # Check if the maximum number of emails per day has been reached
        if emails_sent >= max_emails_per_day:
            print(
                f"Reached the maximum number of emails ({max_emails_per_day}) that can be sent in a day for a free "
                f"Gmail account. Waiting until tomorrow to send more emails.")
            time.sleep(86400)  # Wait for 24 hours (86400 seconds)
            emails_sent = 0

        # Create a new email message
        msg: MIMEMultipart = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.send_message(msg)

        # Increment the number of emails sent in a day
        emails_sent += 1

    # Logout from the Gmail server
    server.quit()
