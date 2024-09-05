from rest_framework import serializers
from .models import FirstStepEvent, UserEvent
from QRScanner.models import Attendee

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'

class FirstStepEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstStepEvent
        fields = '__all__'


class RetrieveFirstStepEvent(serializers.ModelSerializer):
    attendee = AttendeeSerializer()
    # first_step_event = serializers.ReadOnlyField(source='first_step_event.name')
    
    class Meta:
        model = UserEvent 
        fields = ['attendee'] #'created_at'
