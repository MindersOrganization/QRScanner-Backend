from QRScanner.models import Attendee
from rest_framework.views import APIView
from rest_framework.response import Response
from QRScanner.serializer import AttendeeTicketSerializer


class Scan(APIView):
    def post(self, request, uuid, format=None):
        try:
            person = Attendee.objects.get(id=uuid)
            person_serializer = AttendeeTicketSerializer(person)
            if person.has_attended:
                return Response(
                    data={
                        "reason": "This UUID has already been scanned before",
                        "data": person_serializer.data,
                    },
                    status=403
                )
            person.has_attended = True
            person.save()
            return Response(data={
                "data": person_serializer.data
            })
        except Attendee.DoesNotExist:
            return Response(
                data={
                    "reason": "Wrong UUID provided"
                },
                status=404
            )
