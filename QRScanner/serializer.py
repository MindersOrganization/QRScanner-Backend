from rest_framework import serializers
from django.conf import settings
from .models import Attendee


class AttendeeSerializer(serializers.ModelSerializer):
    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = Attendee
        fields = ['id', 'full_name', 'mobile_number', 'email', 'has_attended', 'has_received_email', 'qr_code']

    def get_qr_code(self, obj):
        if obj.qr_code:
            return settings.MEDIA_URL + str(obj.qr_code)
        return None


class AttendeeTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['full_name', 'email', 'mobile_number', 'id']


class AttendeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['has_attended']