from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import get_connection

from QRScanner.models import Attendee
from django.core.management.base import BaseCommand

import time
from datetime import datetime, timedelta


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
    current_time = datetime.now()
    if current_time.hour < 8 or current_time.hour >= 23:
        print("Sleeping until 8 AM.")
        tomorrow = datetime.now() + timedelta(1)
        tomorrow_at_8 = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=8)
        time.sleep((tomorrow_at_8 - datetime.now()).seconds)


def sleep_until_next_hour(curr_hour):
    current_time = datetime.now()
    if curr_hour == current_time.hour:
        next_hour = (current_time + timedelta(hours=1)).replace(minute=0, second=1, microsecond=0)
        sleep_time = (next_hour - current_time).total_seconds()
        time.sleep(sleep_time)
    return current_time.hour


def send_ticket_email(persons):
    subject = "Welcome to First Step!"
    from_email = 'mail@gmail.com'
    with get_connection() as connection:
        counter = 1
        size = len(persons)
        curr_hour = datetime.now().hour
        for person in persons:
            to = person.email
            html_content = render_to_string(
                'ticket.html',
                {
                    'qr_code': "mindersclub.org/qr/api/" + person.qr_code.url
                }
            )

            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")

            time_block()

            msg.send()
            person.has_received_email = True
            person.save()
            print("{}/{} Sent mail to {} at {}".format(counter, size, person.full_name, person.email))
            counter += 1

            if (counter - 1) % 33 == 0:
                print("Sent 20 mails, sleeping for an hour")
                curr_hour = sleep_until_next_hour(curr_hour)


class Command(BaseCommand):
    help = "Send mails to all users who didn't receive ticket mails yet"

    def handle(self, *args, **options):
        try:
            while Attendee.objects.filter(has_received_email=False).exists():
                send_ticket_email(list(Attendee.objects.filter(has_received_email=False)))
        except AttributeError:
            pass
        finally:
            print("Done")
