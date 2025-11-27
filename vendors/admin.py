# Enhanced admin with AI model suggestion button

from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BuildingSystemVendor, AffiliateClick, ModelVendor, ConsultationRequest
from .ai_service import ModelSuggestionService
from django.utils.text import slugify
from django.utils.html import format_html


@admin.register(BuildingSystemVendor)
class BuildingSystemVendorAdmin(admin.ModelAdmin):
    list_display = ('partner_name', 'primary_category', 'is_certified', 'consultation_enabled', 'status', 'model_count', 'created_at')
    list_filter = ('primary_category', 'is_certified', 'consultation_enabled', 'status', 'heal_alignment')
    search_fields = ('partner_name', 'metadata', 'contact_info')
    readonly_fields = ('created_at', 'model_count')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('partner_name', 'primary_category', 'coordinates')
        }),
        ('Affiliate & Consultation', {
            'fields': ('website_url', 'affiliate_link', 'is_certified', 'consultation_enabled')
        }),
        ('Classification', {
            'fields': ('heal_alignment', 'status')
        }),
        ('Additional Data', {
            'fields': ('metadata', 'contact_info', 'created_at', 'model_count'),
            'classes': ('collapse',)
        }),
    )
    
    def model_count(self, obj):
        return obj.models.count()
    model_count.short_description = 'Number of Models'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:vendor_id>/suggest-models/',
                self.admin_site.admin_view(self.suggest_models_view),
                name='vendors_buildingsystemvendor_suggest_models',
            ),
        ]
        return custom_urls + urls
    
    def suggest_models_view(self, request, vendor_id):
        vendor = BuildingSystemVendor.objects.get(pk=vendor_id)
        
        if request.method == 'POST':
            # Generate suggestions and create models
            service = ModelSuggestionService()
            suggestions = service.suggest_models(
                vendor_name=vendor.partner_name,
                website_url=vendor.website_url or ""
            )
            
            created_count = 0
            for model_data in suggestions:
                slug = slugify(model_data['model_name'])
                
                # Check if model already exists
                if not ModelVendor.objects.filter(slug=slug).exists():
                    ModelVendor.objects.create(
                        vendor=vendor,
                        model_name=model_data['model_name'],
                        slug=slug,
                        description=model_data['description'],
                        price_range=model_data.get('price_range', ''),
                        specifications=model_data.get('specifications', {}),
                        is_featured=False
                    )
                    created_count += 1
            
            messages.success(request, f'Created {created_count} models for {vendor.partner_name}')
            return redirect('admin:vendors_buildingsystemvendor_change', vendor_id)
        
        # GET request - show suggestions
        service = ModelSuggestionService()
        suggestions = service.suggest_models(
            vendor_name=vendor.partner_name,
            website_url=vendor.website_url or ""
        )
        
        context = {
            'vendor': vendor,
            'suggestions': suggestions,
            'opts': self.model._meta,
            'has_view_permission': self.has_view_permission(request),
        }
        
        return render(request, 'admin/vendors/suggest_models.html', context)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_suggest_models'] = True
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(AffiliateClick)
class AffiliateClickAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'user', 'timestamp', 'converted')
    list_filter = ('converted', 'timestamp')
    search_fields = ('vendor__partner_name', 'user__username')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'


@admin.register(ModelVendor)
class ModelVendorAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'vendor', 'price_range', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'relationship_type', 'vendor')
    search_fields = ('model_name', 'description', 'vendor__partner_name')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('model_name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('vendor', 'model_name', 'slug', 'description')
        }),
        ('Pricing & Features', {
            'fields': ('price_range', 'is_featured')
        }),
        ('Technical Details', {
            'fields': ('specifications', 'images', 'glb_file', 'relationship_type')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'vendor', 'model', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('email', 'phone', 'message', 'vendor__partner_name', 'model__model_name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('user', 'email', 'phone')
        }),
        ('Context', {
            'fields': ('vendor', 'model', 'message')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
