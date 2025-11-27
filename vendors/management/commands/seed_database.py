"""
Database seeding script for TerraLux Global Building Systems Index.
Seeds vendors from the provided spreadsheet data and uses AI to generate models.
"""

from django.core.management.base import BaseCommand
from vendors.models import BuildingSystemVendor, ModelVendor
from vendors.ai_service import ModelSuggestionService
from django.utils.text import slugify
import time


class Command(BaseCommand):
    help = 'Seed database with vendors and AI-generated models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--vendors-only',
            action='store_true',
            help='Only create vendors, skip model generation',
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit number of vendors to process',
        )

    def handle(self, *args, **options):
        vendors_only = options['vendors_only']
        limit = options.get('limit')
        
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))
        
        # Vendor data from spreadsheet
        vendors_data = [
            {
                "partner_name": "Terra Lux Domes",
                "status": "CORE_COUNCIL",
                "primary_category": "DOMES",
                "website_url": "https://terra-lux.org",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Form & Structure; Engineered geodesic panels for rapid assembly",
                    "region_hq": "USA",
                    "notes": "Proprietary. Designed to integrate with Issho Homes systems"
                }
            },
            {
                "partner_name": "Pacific Domes",
                "status": "ACTIVE",
                "primary_category": "DOMES",
                "website_url": "https://pacificdomes.com",
                "heal_alignment": "MEDIUM",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Geodesic domes for homes, eco-villages, and events",
                    "region_hq": "USA (OR)"
                }
            },
            {
                "partner_name": "ICON Technology Inc.",
                "status": "PRIORITY",
                "primary_category": "3D_PRINT",
                "website_url": "https://iconbuild.com",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Market Leader in 3D-printed homes, robotics, and advanced materials",
                    "region_hq": "USA (TX)",
                    "notes": "Futuristic build method. Aligned with Lennar (Veev)"
                }
            },
            {
                "partner_name": "Phoenix Haus",
                "status": "PRIORITY",
                "primary_category": "PREFAB",
                "website_url": "https://phoenixhaus.com",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Nontoxic, wood-based, Passive-House certified modular systems",
                    "region_hq": "USA (CO)",
                    "notes": "Directly aligns with nontoxic and ultra-healthy interior systems"
                }
            },
            {
                "partner_name": "Plant Prefab",
                "status": "PRIORITY",
                "primary_category": "PREFAB",
                "website_url": "https://plantprefab.com",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "LEED + WELL Certified modular homes. Wellness-focused",
                    "region_hq": "USA (CA)",
                    "notes": "WELL certification is a direct Homes that Heal alignment"
                }
            },
            {
                "partner_name": "ÖÖD House",
                "status": "PRIORITY",
                "primary_category": "PREFAB",
                "website_url": "https://oodhouse.com",
                "heal_alignment": "MEDIUM",
                "is_certified": False,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Luxury prefab mirror-glass modules. High-end showpiece",
                    "region_hq": "Estonia / Global"
                }
            },
            {
                "partner_name": "Cob Cottage Company",
                "status": "PRIORITY",
                "primary_category": "NATURAL",
                "website_url": "https://cobcottage.com",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": False,
                "metadata": {
                    "specialty_focus": "Founders of modern cob revival. Ideal for education/workshops",
                    "region_hq": "USA (OR)",
                    "notes": "Inherently low-toxicity, natural, ancient method"
                }
            },
            {
                "partner_name": "Earthship Biotecture",
                "status": "PRIORITY",
                "primary_category": "NATURAL",
                "website_url": "https://earthshipglobal.com",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Recycled-material, passive thermal mass, off-grid autonomous homes",
                    "region_hq": "USA (NM)",
                    "notes": "Focus on autonomy, recycling, and passive systems"
                }
            },
            {
                "partner_name": "Deltec Homes",
                "status": "PRIORITY",
                "primary_category": "DOMES",
                "website_url": "https://deltechomes.com",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Circular (round) prefab homes; toxin-free materials, hurricane-proof",
                    "region_hq": "USA (NC)",
                    "notes": "Toxin-free materials and resilience are direct Heal alignments"
                }
            },
            {
                "partner_name": "Baumraum",
                "status": "PRIORITY",
                "primary_category": "TREE",
                "website_url": "https://baumraum.de",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "High-design, luxury tree-integrated architecture",
                    "region_hq": "Germany",
                    "notes": "Direct biophilic connection. Ideal for Experiential Stays"
                }
            },
            {
                "partner_name": "Arkup",
                "status": "PRIORITY",
                "primary_category": "PREFAB",
                "website_url": "https://arkup.com",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Luxury, solar-powered, self-elevating livable yachts",
                    "region_hq": "USA (FL)",
                    "notes": "Futuristic, off-grid, resilient. Ideal Experiential Stay showpiece"
                }
            },
            {
                "partner_name": "Method Homes",
                "status": "PRIORITY",
                "primary_category": "PREFAB",
                "website_url": "https://methodhomes.net",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Modern sustainable prefab; can build to Passive House/LBC standards",
                    "region_hq": "USA"
                }
            },
            {
                "partner_name": "Huf Haus",
                "status": "PRIORITY",
                "primary_category": "PREFAB",
                "website_url": "https://huf-haus.com",
                "heal_alignment": "MEDIUM",
                "is_certified": False,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "High-end, customizable timber-and-glass prefab homes",
                    "region_hq": "Germany"
                }
            },
            {
                "partner_name": "CORE (Climate-Oriented Real Estate)",
                "status": "PRIORITY",
                "primary_category": "PREFAB",
                "website_url": "https://core-we-care.com",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Sustainable/regenerative prefab with a no glues or chemicals focus",
                    "region_hq": "Canada (BC)",
                    "notes": "Healthy Low-Tech High-Performance Buildings. Perfect mission alignment"
                }
            },
            {
                "partner_name": "Monolithic Dome Institute",
                "status": "PRIORITY",
                "primary_category": "DOMES",
                "website_url": "https://monolithic.com",
                "heal_alignment": "MEDIUM",
                "is_certified": False,
                "consultation_enabled": True,
                "metadata": {
                    "specialty_focus": "Reinforced concrete domes; highly durable, efficient, and resilient",
                    "region_hq": "USA (TX)"
                }
            },
        ]
        
        # Process vendors
        created_count = 0
        for i, vendor_data in enumerate(vendors_data):
            if limit and i >= limit:
                break
                
            # Check if vendor already exists
            if BuildingSystemVendor.objects.filter(partner_name=vendor_data['partner_name']).exists():
                self.stdout.write(self.style.WARNING(f"Vendor '{vendor_data['partner_name']}' already exists, skipping"))
                continue
            
            # Create vendor
            vendor = BuildingSystemVendor.objects.create(**vendor_data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"✓ Created vendor: {vendor.partner_name}"))
            
            # Generate models with AI (unless vendors-only flag is set)
            if not vendors_only and vendor.website_url:
                self.stdout.write(f"  Generating models for {vendor.partner_name}...")
                try:
                    service = ModelSuggestionService()
                    suggestions = service.suggest_models(
                        vendor_name=vendor.partner_name,
                        website_url=vendor.website_url
                    )
                    
                    model_count = 0
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
                            model_count += 1
                    
                    self.stdout.write(self.style.SUCCESS(f"  ✓ Created {model_count} models"))
                    
                    # Rate limiting to avoid API throttling
                    time.sleep(2)
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  ✗ Error generating models: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Seeding complete! Created {created_count} vendors'))
