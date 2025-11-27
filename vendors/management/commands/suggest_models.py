"""
Management command to suggest models for a vendor using AI.

Usage:
    python manage.py suggest_models <vendor_id>
    python manage.py suggest_models <vendor_id> --auto-create
"""

from django.core.management.base import BaseCommand
from vendors.models import BuildingSystemVendor, ModelVendor
from vendors.ai_service import ModelSuggestionService
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Suggest building models for a vendor using AI'

    def add_arguments(self, parser):
        parser.add_argument('vendor_id', type=int, help='ID of the vendor')
        parser.add_argument(
            '--auto-create',
            action='store_true',
            help='Automatically create the suggested models in the database',
        )

    def handle(self, *args, **options):
        vendor_id = options['vendor_id']
        auto_create = options['auto_create']
        
        try:
            vendor = BuildingSystemVendor.objects.get(id=vendor_id)
        except BuildingSystemVendor.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Vendor with ID {vendor_id} not found'))
            return
        
        self.stdout.write(f'Generating model suggestions for: {vendor.partner_name}')
        self.stdout.write(f'Website: {vendor.website_url or "No website provided"}')
        
        # Get AI suggestions
        service = ModelSuggestionService()
        suggestions = service.suggest_models(
            vendor_name=vendor.partner_name,
            website_url=vendor.website_url or ""
        )
        
        if not suggestions:
            self.stdout.write(self.style.WARNING('No suggestions generated'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'\nGenerated {len(suggestions)} model suggestions:\n'))
        
        for i, model_data in enumerate(suggestions, 1):
            self.stdout.write(f"\n{i}. {model_data['model_name']}")
            self.stdout.write(f"   Description: {model_data['description']}")
            self.stdout.write(f"   Price Range: {model_data.get('price_range', 'N/A')}")
            self.stdout.write(f"   Specifications: {model_data.get('specifications', {})}")
            
            if auto_create:
                # Create the model
                slug = slugify(model_data['model_name'])
                
                # Check if model with this slug already exists
                if ModelVendor.objects.filter(slug=slug).exists():
                    self.stdout.write(self.style.WARNING(f"   ⚠ Model with slug '{slug}' already exists, skipping"))
                    continue
                
                model = ModelVendor.objects.create(
                    vendor=vendor,
                    model_name=model_data['model_name'],
                    slug=slug,
                    description=model_data['description'],
                    price_range=model_data.get('price_range', ''),
                    specifications=model_data.get('specifications', {}),
                    is_featured=False
                )
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created model: {model.model_name}"))
        
        if not auto_create:
            self.stdout.write(self.style.WARNING('\n\nTo automatically create these models, run with --auto-create flag'))
