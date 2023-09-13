from django.shortcuts import render
from rest_framework import viewsets
from QRScanner.models import Attendee
from QRScanner.serializer import QRScannerTestSerializer


# Create your views here.

class QRScannerTestViewSet(
    viewsets.ModelViewSet,
):
    queryset = Attendee.objects.all()
    serializer_class = QRScannerTestSerializer
    lookup_field = 'id'
