from rest_framework.serializers import ModelSerializer

from QRScanner.models import Attendee


class AttendeeTicketSerializer(ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['full_name', 'email', 'mobile_number', 'id']
