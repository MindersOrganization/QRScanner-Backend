import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import get_connection

from QRScanner.models import PotentialAttendee

from django.core.management.base import BaseCommand


def send_marketing_email(persons):
    subject = """Join us at "First Step" Event - Style your future"""
    from_email = 'mail@gmail.com'
    with get_connection() as connection:
        counter = 1
        size = len(persons)
        for person in persons:
            to = person.email
            html_content = render_to_string('marketing_mail.html', {'full_name': person.full_name})
            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("({}/{}) -> Sent mail to {}.".format(counter, size, person.full_name))
            counter += 1

            if (counter - 1) % 20 == 0:
                print("Mails are sent, sleeping for an hour")
                time.sleep(3600)


class Command(BaseCommand):
    help = "Send marketing mails to potential attendees"

    def handle(self, *args, **options):
        send_marketing_email(PotentialAttendee.objects.all())
