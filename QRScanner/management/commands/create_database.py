import csv
from QRScanner.models import Person
from django.core.management.base import BaseCommand


def csv_to_db(file: str) -> None:
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            obj = Person(
                mobile_number=row['mobile_number'],
                email=row['email'],
                full_name=row['full_name']
            )
            obj.save()


class Command(BaseCommand):
    help = "Send mails to all users who didn't receive mails yet"

    def handle(self, *args, **options):
        print("Importing CSV ...")
        csv_to_db(".\\Scripts\\data.csv")
        print("Finished Successfully")
