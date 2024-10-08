from QRScanner.models import Attendee
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from QRScanner.serializer import AttendeeTicketSerializer, AttendeeUpdateSerializer
from QRScanner.serializer import AttendeeSerializer
from django_filters import rest_framework as filters


class AttendeeFilter(filters.FilterSet):
    full_name = filters.CharFilter(lookup_expr='icontains')
    mobile_number = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    has_attended = filters.BooleanFilter(lookup_expr='exact')
    has_received_email = filters.BooleanFilter(lookup_expr='exact')


class AttendeeListView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Attendee.objects.order_by('full_name').all()
    serializer_class = AttendeeSerializer
    lookup_field = 'id'
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AttendeeFilter

    def update(self, request, *args, **kwargs):
        temp_serializer_class = self.serializer_class
        temp_filter_backend = self.filter_backends
        temp_filterset_class = self.filterset_class
        self.serializer_class = AttendeeUpdateSerializer
        ret = super().update(request, *args, **kwargs)
        self.serializer_class = temp_serializer_class
        self.filter_backends = temp_filter_backend
        self.filterset_class = self.filterset_class
        return ret


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
