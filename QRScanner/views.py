from django.shortcuts import render
from rest_framework import mixins, viewsets
from QRScanner.models import Attendee
from QRScanner.serializer import AttendeeSerializer
from django_filters import rest_framework as filters


class AttendeeFilter(filters.FilterSet):
    full_name = filters.CharFilter(lookup_expr='icontains')
    mobile_number = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    has_attended = filters.BooleanFilter(lookup_expr='exact')
    has_received_email = filters.BooleanFilter(lookup_expr='exact')


# Create your views here.


class AttendeeListView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Attendee.objects.order_by('full_name').all()
    serializer_class = AttendeeSerializer
    lookup_field = 'id'
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AttendeeFilter
