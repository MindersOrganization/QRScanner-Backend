from rest_framework.serializers import ModelSerializer

from QRScanner.models import Attendee


class QRScannerTestSerializer(ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'
