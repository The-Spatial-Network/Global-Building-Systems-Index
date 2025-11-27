from rest_framework import serializers
from .models import BuildingSystemVendor, AffiliateClick, ModelVendor, ConsultationRequest

class BuildingSystemVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingSystemVendor
        fields = '__all__'

class AffiliateClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateClick
        fields = '__all__'

class ModelVendorListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for model listings"""
    vendor_name = serializers.CharField(source='vendor.partner_name', read_only=True)
    
    class Meta:
        model = ModelVendor
        fields = ['id', 'model_name', 'slug', 'vendor', 'vendor_name', 'price_range', 'is_featured', 'images']

class ModelVendorSerializer(serializers.ModelSerializer):
    """Full serializer for model details"""
    vendor_name = serializers.CharField(source='vendor.partner_name', read_only=True)
    vendor_data = BuildingSystemVendorSerializer(source='vendor', read_only=True)
    
    class Meta:
        model = ModelVendor
        fields = '__all__'

class ConsultationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationRequest
        fields = ['id', 'email', 'phone', 'vendor', 'model', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']
