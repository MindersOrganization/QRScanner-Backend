import smtplib
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import get_connection

from QRScanner.models import Attendee
from django.core.management.base import BaseCommand

import time
from datetime import datetime, timedelta
import pytz


def attach_qr_code(msg, person):
    # Open the image file in binary mode
    with open(person.qr_code.path, 'rb') as img:
        # Create a MIMEImage
        msg_img = MIMEImage(img.read(), _subtype='png')
        # Define the Content-ID header
        msg_img.add_header('Content-ID', '<qr_code>')
        # Attach the image
        msg.attach(msg_img)
    return msg


def time_block():
    cairo_tz = pytz.timezone('Africa/Cairo')
    current_time = datetime.now(cairo_tz)
    if current_time.hour < 8 or current_time.hour >= 23:
        print("Sleeping until 8 AM.")
        tomorrow = datetime.now(cairo_tz) + timedelta(1)
        tomorrow_at_8 = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=8, tzinfo=cairo_tz)
        time.sleep((tomorrow_at_8 - datetime.now(cairo_tz)).seconds)


def send_ticket_email(persons):
    subject = "Welcome to First Step!"
    from_email = 'minders.fcih@gmail.com'
    with get_connection() as connection:
        person = persons[0]
        to = person.email
        html_content = render_to_string(
            'ticket.html',
            {
                'qr_code': "mindersclub.org/qr/api/" + person.qr_code.url
            }
        )

        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")

        # time_block()

        try:
            msg.send()
            print("Sent mail to {} at {}".format(person.full_name, person.email))
        except smtplib.SMTPRecipientsRefused:
            print("Failed mail to {} at {}, Skipping.".format(person.full_name, person.email))

        person.has_received_email = True
        person.save()


class Command(BaseCommand):
    help = "Send mails to all users who didn't receive ticket mails yet"

    def handle(self, *args, **options):
        while Attendee.objects.filter(has_received_email=False).exists():
            try:
                send_ticket_email(list(Attendee.objects.filter(has_received_email=False)))
            except AttributeError:
                pass
            except smtplib.SMTPServerDisconnected:
                print("Disconnected, Sleeping for 30 seconds this attempting again")
                time.sleep(30)
            finally:
                time.sleep(2)
        print("Done")
