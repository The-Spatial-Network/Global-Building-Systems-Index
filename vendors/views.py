from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BuildingSystemVendor, AffiliateClick, ModelVendor, ConsultationRequest
from .serializers import (
    BuildingSystemVendorSerializer, 
    AffiliateClickSerializer,
    ModelVendorSerializer,
    ModelVendorListSerializer,
    ConsultationRequestSerializer
)

class VendorViewSet(viewsets.ModelViewSet):
    queryset = BuildingSystemVendor.objects.all()
    serializer_class = BuildingSystemVendorSerializer

    @action(detail=True, methods=['post'])
    def track_click(self, request, pk=None):
        vendor = self.get_object()
        user = request.user if request.user.is_authenticated else None
        
        click = AffiliateClick.objects.create(
            vendor=vendor,
            user=user
        )
        
        return Response({'status': 'click tracked', 'click_id': click.id}, status=status.HTTP_201_CREATED)

class ModelVendorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelVendor.objects.select_related('vendor').all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ModelVendorListSerializer
        return ModelVendorSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor', None)
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset

class ConsultationRequestViewSet(viewsets.ModelViewSet):
    queryset = ConsultationRequest.objects.all()
    serializer_class = ConsultationRequestSerializer
    http_method_names = ['post']  # Only allow POST for visitors
    
    def create(self, request, *args, **kwargs):
        # Attach authenticated user if available
        if request.user.is_authenticated:
            request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)
