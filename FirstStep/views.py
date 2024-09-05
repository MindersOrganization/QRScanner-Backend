import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FirstStepEvent, UserEvent
from QRScanner.models import Attendee
from rest_framework import generics
from .serializers import (
    FirstStepEventSerializer,
    RetrieveFirstStepEvent
)

class FirstStepEventListCreateAPIView(generics.ListCreateAPIView):
    queryset = FirstStepEvent.objects.all()
    serializer_class = FirstStepEventSerializer

class FirstStepEventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FirstStepEvent.objects.all()
    serializer_class = FirstStepEventSerializer
      
# retrieve the evnet with there attendee
class GroupUsersListAPIView(generics.ListAPIView):
    serializer_class = RetrieveFirstStepEvent

    def get_queryset(self):
        event_id = self.kwargs['pk']
        return UserEvent.objects.filter(first_step_event=event_id).select_related('attendee')   
         
class UploadAttendeesView(APIView):
    def post(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        file = request.FILES.get('file')

        if not event_id or not file:
            return Response({"error": "Event ID and file are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = FirstStepEvent.objects.get(id=event_id)
        except FirstStepEvent.DoesNotExist:
            return Response({"error": "Event with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file)
            elif file.name.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file)
            else:
                return Response({"error": "Unsupported file format."}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure required columns are present
            required_columns = {'mobile_number', 'email', 'full_name'}
            if not required_columns.issubset(data.columns):
                return Response({"error": f"Missing required columns: {required_columns - set(data.columns)}"}, status=status.HTTP_400_BAD_REQUEST)
            print (data)
            # Process each row
            for _, row in data.iterrows():
                print (row)
                
                attendee = Attendee(
                    full_name=row['full_name'],
                    mobile_number=row['mobile_number'],
                    email=row['email'],
                )
                attendee.save()
                
                UserEvent.objects.create(
                    first_step_event=event,
                    attendee=attendee,
                )

            return Response({"message": "Attendees created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
