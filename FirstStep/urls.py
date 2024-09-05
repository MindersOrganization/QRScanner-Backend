from django.urls import path
from .views import (
    FirstStepEventListCreateAPIView, 
    FirstStepEventRetrieveUpdateDestroyAPIView,
    UploadAttendeesView,
    GroupUsersListAPIView,
)

urlpatterns = [
    path('', FirstStepEventListCreateAPIView.as_view(), name='first-step-event-list-create'),
    path('<int:pk>/', FirstStepEventRetrieveUpdateDestroyAPIView.as_view(), name='first-step-event-detail'),
    path('upload-attendees/', UploadAttendeesView.as_view(), name='upload-attendees'),
    path('<int:pk>/get_event_attendee/', GroupUsersListAPIView.as_view(), name='event_attendee')
]
