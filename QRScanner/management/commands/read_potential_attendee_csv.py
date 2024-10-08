import csv
from QRScanner.models import PotentialAttendee
from django.core.management.base import BaseCommand


def csv_to_db(file: str) -> None:
    with open(file, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            obj = PotentialAttendee(
                mobile_number=row['mobile_number'],
                email=row['email'],
                full_name=row['full_name']
            )
            obj.save()


class Command(BaseCommand):
    help = "Import database from potential_attendee.csv file in the project's root directory"

    def handle(self, *args, **options):
        print("Importing CSV ...")
        csv_to_db("./data/potential_attendee.csv")
        print("Finished Successfully")
