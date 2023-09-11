import time
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import get_connection

from QRScanner.models import Person

from django.core.management.base import BaseCommand


def send_ticket_email(persons):
    subject = "Minders'23 First Step - Style Your Future"
    from_email = 'mail@gmail.com'
    with get_connection() as connection:
        for person in persons:
            to = person.email
            html_content = render_to_string('ticket.html', {'full_name': person.full_name})

            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")

            # Open the image file in binary mode
            with open(person.qr_code.path, 'rb') as img:
                # Create a MIMEImage
                msg_img = MIMEImage(img.read(), _subtype='png')
                # Define the Content-ID header
                msg_img.add_header('Content-ID', '<qr_code>')
                # Attach the image
                msg.attach(msg_img)

            msg.send()
            person.has_received_email = True
            person.save()
            print("Sent mail to {}.".format(person.full_name))

        if persons.index(person) % 20 == 0:
            time.sleep(3600)


class Command(BaseCommand):
    help = "Send mails to all users who didn't receive mails yet"

    def handle(self, *args, **options):
        while Person.objects.filter(has_received_email=False).exists():
            send_ticket_email(Person.objects.filter(has_received_email=False)[:20])
