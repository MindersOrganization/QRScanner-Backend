from django.urls import include, path
from QRScanner import views

urlpatterns = [
    path('<uuid:uuid>/', views.Scan.as_view(), name='scan'),
]
