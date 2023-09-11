from django.shortcuts import render
from rest_framework import viewsets
from QRScanner.models import Person
from QRScanner.serializer import QRScannerTestSerializer


# Create your views here.

class QRScannerTestViewSet(
    viewsets.ModelViewSet,
):
    queryset = Person.objects.all()
    serializer_class = QRScannerTestSerializer
    lookup_field = 'id'
