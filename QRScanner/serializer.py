from rest_framework.serializers import ModelSerializer

from QRScanner.models import Person


class QRScannerTestSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
