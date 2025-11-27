"""
Comprehensive database seeding with realistic model data for all vendors.
This script includes predefined models based on research for each vendor.
"""

from django.core.management.base import BaseCommand
from vendors.models import BuildingSystemVendor, ModelVendor
from django.utils.text import slugify


# Realistic model data for key vendors
VENDOR_MODELS = {
    "Pacific Domes": [
        {
            "model_name": "24ft Geodesic Dome",
            "description": "A versatile 24-foot diameter geodesic dome perfect for eco-villages, glamping sites, and off-grid living. Features sustainable timber framing and can be customized with various covering options.",
            "price_range": "$15k-$25k",
            "specifications": {
                "diameter": "24 feet",
                "floor_area": "452 sq ft",
                "height": "12 feet",
                "capacity": "2-4 people",
                "materials": "Douglas fir timber frame",
                "covering_options": "Canvas, vinyl, or insulated panels"
            },
            "is_featured": True
        },
        {
            "model_name": "30ft Geodesic Dome",
            "description": "Spacious 30-foot geodesic dome ideal for permanent residences or retreat centers. Offers excellent structural integrity and energy efficiency with its spherical design.",
            "price_range": "$25k-$40k",
            "specifications": {
                "diameter": "30 feet",
                "floor_area": "707 sq ft",
                "height": "15 feet",
                "capacity": "4-6 people",
                "materials": "Engineered timber frame",
                "insulation": "R-30 available"
            },
            "is_featured": False
        },
        {
            "model_name": "Event Dome 40ft",
            "description": "Large-scale event dome perfect for weddings, festivals, and community gatherings. Quick assembly and stunning visual impact.",
            "price_range": "$40k-$60k",
            "specifications": {
                "diameter": "40 feet",
                "floor_area": "1,257 sq ft",
                "height": "20 feet",
                "capacity": "50-100 people",
                "setup_time": "2-3 days",
                "materials": "Heavy-duty aluminum frame"
            },
            "is_featured": False
        }
    ],
    "ICON Technology Inc.": [
        {
            "model_name": "House Zero",
            "description": "ICON's flagship 3D-printed home featuring advanced robotics and sustainable materials. Zero-energy ready with integrated solar and battery systems.",
            "price_range": "$200k-$300k",
            "specifications": {
                "size": "1,500-2,000 sq ft",
                "bedrooms": "2-3",
                "bathrooms": "2",
                "construction_time": "5-7 days print time",
                "materials": "Lavacrete (proprietary concrete mix)",
                "energy": "Net-zero ready"
            },
            "is_featured": True
        },
        {
            "model_name": "Community Print",
            "description": "Affordable 3D-printed home designed for community-scale developments. Optimized for rapid deployment and cost efficiency.",
            "price_range": "$99k-$150k",
            "specifications": {
                "size": "800-1,200 sq ft",
                "bedrooms": "2",
                "bathrooms": "1-2",
                "construction_time": "24 hours print time",
                "materials": "Lavacrete",
                "warranty": "50+ year structural"
            },
            "is_featured": False
        }
    ],
    "Phoenix Haus": [
        {
            "model_name": "Passive House Studio",
            "description": "Ultra-efficient studio ADU built to Passive House standards. Features non-toxic materials and exceptional air quality systems.",
            "price_range": "$150k-$200k",
            "specifications": {
                "size": "600 sq ft",
                "bedrooms": "Studio",
                "bathrooms": "1",
                "energy_use": "90% less than code",
                "materials": "FSC-certified wood, zero-VOC finishes",
                "ventilation": "ERV with HEPA filtration"
            },
            "is_featured": True
        },
        {
            "model_name": "Family Home 1800",
            "description": "Spacious Passive House certified family home with open floor plan and abundant natural light. Nontoxic throughout.",
            "price_range": "$400k-$550k",
            "specifications": {
                "size": "1,800 sq ft",
                "bedrooms": "3",
                "bathrooms": "2.5",
                "energy_use": "85% less than code",
                "materials": "Solid wood construction, natural finishes",
                "certification": "Passive House Institute US"
            },
            "is_featured": False
        }
    ],
    "Plant Prefab": [
        {
            "model_name": "LivingHome 1",
            "description": "LEED Platinum and WELL Certified prefab home with focus on wellness and sustainability. Features circadian lighting and advanced air filtration.",
            "price_range": "$350k-$500k",
            "specifications": {
                "size": "1,200 sq ft",
                "bedrooms": "2",
                "bathrooms": "2",
                "certifications": "LEED Platinum, WELL Gold",
                "materials": "Low-VOC, sustainable sourced",
                "features": "Circadian lighting, HEPA filtration"
            },
            "is_featured": True
        },
        {
            "model_name": "Accessory Dwelling Unit",
            "description": "Compact ADU perfect for multigenerational living or rental income. LEED certified with wellness features.",
            "price_range": "$200k-$280k",
            "specifications": {
                "size": "640 sq ft",
                "bedrooms": "1",
                "bathrooms": "1",
                "construction_time": "6-8 weeks",
                "certifications": "LEED Gold",
                "energy": "All-electric, solar-ready"
            },
            "is_featured": False
        }
    ],
    "ÖÖD House": [
        {
            "model_name": "ÖÖD 1",
            "description": "Iconic mirror-glass prefab module. Minimalist luxury with stunning reflective exterior that blends with nature.",
            "price_range": "$120k-$180k",
            "specifications": {
                "size": "290 sq ft",
                "bedrooms": "Studio",
                "bathrooms": "1",
                "delivery_time": "8-12 weeks",
                "materials": "Mirror glass exterior, wood interior",
                "mobility": "Relocatable on trailer"
            },
            "is_featured": True
        },
        {
            "model_name": "ÖÖD 2",
            "description": "Expanded two-module configuration offering more space while maintaining the signature mirror aesthetic.",
            "price_range": "$200k-$280k",
            "specifications": {
                "size": "580 sq ft",
                "bedrooms": "1",
                "bathrooms": "1",
                "configuration": "Two connected modules",
                "materials": "Mirror glass, premium wood",
                "features": "Smart home integration"
            },
            "is_featured": False
        }
    ],
    "Terra Lux Domes": [
        {
            "model_name": "Engineered Geodesic Panel System",
            "description": "Proprietary engineered panel system for rapid geodesic dome assembly. Designed to integrate seamlessly with Issho Homes wellness systems.",
            "price_range": "$30k-$50k",
            "specifications": {
                "diameter": "20-30 feet",
                "panel_type": "Engineered composite",
                "assembly_time": "2-4 days",
                "integration": "Issho Homes compatible",
                "insulation": "R-40 panels available",
                "warranty": "25 years structural"
            },
            "is_featured": True
        }
    ],
    "Earthship Biotecture": [
        {
            "model_name": "Global Model Earthship",
            "description": "The classic Earthship design featuring recycled tire walls, passive solar heating/cooling, and complete off-grid systems.",
            "price_range": "$250k-$400k",
            "specifications": {
                "size": "1,500-2,500 sq ft",
                "bedrooms": "2-3",
                "bathrooms": "2",
                "walls": "Rammed earth tires",
                "systems": "Rainwater, greywater, solar, food production",
                "climate": "Works in any climate"
            },
            "is_featured": True
        },
        {
            "model_name": "Simple Survival Model",
            "description": "Streamlined Earthship design for those seeking essential off-grid living at a lower price point.",
            "price_range": "$100k-$180k",
            "specifications": {
                "size": "800-1,200 sq ft",
                "bedrooms": "1-2",
                "bathrooms": "1",
                "walls": "Rammed earth tires",
                "systems": "Basic off-grid package",
                "ideal_for": "Single person or couple"
            },
            "is_featured": False
        }
    ],
    "Deltec Homes": [
        {
            "model_name": "Renew Series 1200",
            "description": "Circular prefab home with toxin-free materials and hurricane-resistant design. Net-zero energy capable.",
            "price_range": "$280k-$380k",
            "specifications": {
                "size": "1,200 sq ft",
                "bedrooms": "2",
                "bathrooms": "2",
                "shape": "Circular (round)",
                "wind_rating": "Category 5 hurricane",
                "materials": "Toxin-free, sustainable",
                "energy": "Net-zero ready"
            },
            "is_featured": True
        }
    ],
    "Baumraum": [
        {
            "model_name": "Djuren Treehouse",
            "description": "Luxury treehouse with panoramic windows and suspended design. Perfect integration with forest canopy.",
            "price_range": "$180k-$280k",
            "specifications": {
                "size": "400-600 sq ft",
                "bedrooms": "1",
                "bathrooms": "1",
                "elevation": "10-25 feet",
                "materials": "Sustainable timber, large-format glass",
                "features": "Heated floors, full kitchen"
            },
            "is_featured": True
        }
    ],
    "Arkup": [
        {
            "model_name": "Arkup 75",
            "description": "Luxury floating villa with solar power, rainwater collection, and hydraulic stilts for stability. The ultimate in waterfront living.",
            "price_range": "$5.5M-$7M",
            "specifications": {
                "size": "4,350 sq ft",
                "bedrooms": "4",
                "bathrooms": "4.5",
                "power": "Solar + battery (off-grid capable)",
                "water": "Rainwater + desalination",
                "mobility": "Self-propelled, relocatable",
                "features": "Hydraulic stilts, rooftop terrace"
            },
            "is_featured": True
        }
    ]
}


class Command(BaseCommand):
    help = 'Seed database with comprehensive vendor and model data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            ModelVendor.objects.all().delete()
            BuildingSystemVendor.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Data cleared'))
        
        self.stdout.write(self.style.SUCCESS('Starting comprehensive database seeding...'))
        
        # All vendor data
        vendors_data = [
            {
                "partner_name": "Terra Lux Domes",
                "status": "CORE_COUNCIL",
                "primary_category": "DOMES",
                "website_url": "https://terra-lux.org",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "coordinates": "37.7749,-122.4194",  # SF coordinates as placeholder
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
                "affiliate_link": "https://pacificdomes.com/?ref=terralux",
                "heal_alignment": "MEDIUM",
                "is_certified": True,
                "consultation_enabled": True,
                "coordinates": "45.5152,-122.6784",  # Portland, OR
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
                "affiliate_link": "https://iconbuild.com/?ref=terralux",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "coordinates": "30.2672,-97.7431",  # Austin, TX
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
                "affiliate_link": "https://phoenixhaus.com/?ref=terralux",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "coordinates": "39.7392,-104.9903",  # Denver, CO
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
                "affiliate_link": "https://plantprefab.com/?ref=terralux",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "coordinates": "34.0522,-118.2437",  # Los Angeles, CA
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
                "affiliate_link": "https://oodhouse.com/?ref=terralux",
                "heal_alignment": "MEDIUM",
                "is_certified": False,
                "consultation_enabled": True,
                "coordinates": "59.4370,24.7536",  # Tallinn, Estonia
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
                "coordinates": "44.0521,-123.0868",  # Eugene, OR
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
                "affiliate_link": "https://earthshipglobal.com/?ref=terralux",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "coordinates": "36.4072,-105.5731",  # Taos, NM
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
                "affiliate_link": "https://deltechomes.com/?ref=terralux",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "coordinates": "35.5951,-82.5515",  # Asheville, NC
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
                "affiliate_link": "https://baumraum.de/?ref=terralux",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "coordinates": "53.5511,9.9937",  # Hamburg, Germany
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
                "affiliate_link": "https://arkup.com/?ref=terralux",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "coordinates": "25.7617,-80.1918",  # Miami, FL
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
                "affiliate_link": "https://methodhomes.net/?ref=terralux",
                "heal_alignment": "HIGH",
                "is_certified": True,
                "consultation_enabled": True,
                "coordinates": "47.6062,-122.3321",  # Seattle, WA
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
                "affiliate_link": "https://huf-haus.com/?ref=terralux",
                "heal_alignment": "MEDIUM",
                "is_certified": False,
                "consultation_enabled": True,
                "coordinates": "50.3569,7.5890",  # Koblenz, Germany
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
                "coordinates": "49.2827,-123.1207",  # Vancouver, BC
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
                "coordinates": "32.3513,-95.3011",  # Tyler, TX
                "metadata": {
                    "specialty_focus": "Reinforced concrete domes; highly durable, efficient, and resilient",
                    "region_hq": "USA (TX)"
                }
            },
        ]
        
        # Create vendors and models
        vendor_count = 0
        model_count = 0
        
        for vendor_data in vendors_data:
            # Check if vendor exists
            vendor, created = BuildingSystemVendor.objects.get_or_create(
                partner_name=vendor_data['partner_name'],
                defaults=vendor_data
            )
            
            if created:
                vendor_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created vendor: {vendor.partner_name}"))
                
                # Add models if we have predefined data
                if vendor.partner_name in VENDOR_MODELS:
                    for model_data in VENDOR_MODELS[vendor.partner_name]:
                        slug = slugify(model_data['model_name'])
                        model, model_created = ModelVendor.objects.get_or_create(
                            slug=slug,
                            defaults={
                                'vendor': vendor,
                                **model_data
                            }
                        )
                        if model_created:
                            model_count += 1
                            self.stdout.write(f"  ✓ Created model: {model.model_name}")
            else:
                self.stdout.write(self.style.WARNING(f"Vendor '{vendor.partner_name}' already exists"))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Seeding complete!'))
        self.stdout.write(self.style.SUCCESS(f'  Created {vendor_count} vendors'))
        self.stdout.write(self.style.SUCCESS(f'  Created {model_count} models'))
