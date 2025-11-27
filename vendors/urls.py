from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, ModelVendorViewSet, ConsultationRequestViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'models', ModelVendorViewSet)
router.register(r'consultations', ConsultationRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
