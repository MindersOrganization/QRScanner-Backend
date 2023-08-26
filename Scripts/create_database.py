import csv
from QRScanner.models import Person


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
