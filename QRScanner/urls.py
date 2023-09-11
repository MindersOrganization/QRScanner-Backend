from django.urls import include, path
from rest_framework import routers
from QRScanner import views

router = routers.DefaultRouter()
router.register('', views.QRScannerTestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
