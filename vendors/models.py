from django.db import models
from django.contrib.postgres.fields import ArrayField

class BuildingSystemVendor(models.Model):
    CATEGORY_CHOICES = [
        ('PREFAB', 'Prefab & Modular'),
        ('NATURAL', 'Natural & Earthen'),
        ('DOMES', 'Domes & Shells'),
        ('3D_PRINT', '3D Printed'),
        ('TREE', 'Tree Homes'),
        ('HEALTHY', 'Healthy Systems'),
        ('COMMUNITY', 'Community'),
    ]

    HEAL_ALIGNMENT_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    STATUS_CHOICES = [
        ('CORE_COUNCIL', 'Core Council'),
        ('PRIORITY', 'Priority Prospect'),
        ('ACTIVE', 'Active Vendor'),
    ]

    partner_name = models.CharField(max_length=255)
    website_url = models.URLField(max_length=500, blank=True, null=True)
    affiliate_link = models.URLField(max_length=500, blank=True, null=True, help_text="The specific URL with TerraLux tracking parameters.")
    is_certified = models.BooleanField(default=False, help_text="If TRUE, displays 'Certified Partner' badge.")
    consultation_enabled = models.BooleanField(default=False, help_text="If TRUE, shows the 'Schedule Consultation' button.")
    # Temporarily using simple coordinates instead of PostGIS PointField
    coordinates = models.CharField(max_length=100, blank=True, help_text="Lat,Lng format")
    primary_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    heal_alignment = models.CharField(max_length=20, choices=HEAL_ALIGNMENT_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    metadata = models.JSONField(default=dict, blank=True)
    contact_info = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.partner_name

class AffiliateClick(models.Model):
    vendor = models.ForeignKey(BuildingSystemVendor, on_delete=models.CASCADE, related_name='clicks')
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    converted = models.BooleanField(default=False)

    def __str__(self):
        return f"Click on {self.vendor.partner_name} at {self.timestamp}"

class ModelVendor(models.Model):
    vendor = models.ForeignKey(BuildingSystemVendor, on_delete=models.CASCADE, related_name='models')
    model_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly identifier")
    description = models.TextField(blank=True, help_text="Detailed product description")
    price_range = models.CharField(max_length=100, blank=True, help_text="e.g., '$50k-$100k'")
    specifications = models.JSONField(default=dict, blank=True, help_text="Technical specifications")
    images = models.JSONField(default=list, blank=True, help_text="List of image URLs")
    is_featured = models.BooleanField(default=False, help_text="Highlight this model")
    glb_file = models.FileField(upload_to='models_3d/', blank=True, null=True)
    relationship_type = models.CharField(max_length=50, default='Manufacturer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = 'Building Model'
        verbose_name_plural = 'Building Models'

    def __str__(self):
        return f"{self.vendor.partner_name} - {self.model_name}"

class ConsultationRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONTACTED', 'Contacted'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_requests')
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    vendor = models.ForeignKey(BuildingSystemVendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_requests')
    model = models.ForeignKey(ModelVendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_requests')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consultation Request'
        verbose_name_plural = 'Consultation Requests'

    def __str__(self):
        context = ""
        if self.vendor:
            context = f" (Vendor: {self.vendor.partner_name})"
        elif self.model:
            context = f" (Model: {self.model.model_name})"
        return f"Consultation from {self.email}{context}"
