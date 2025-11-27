# TerraLux Global Building Systems Index

A streamlined application serving as the "Google" of regenerative construction, aggregating the world's best sustainable building technologies into a single, searchable catalogue.

## Features

### For Visitors
- **Living Catalogue**: Browse certified vendors and sustainable building technologies
- **Advanced Search & Filtering**: Find vendors by category, region, and certification status
- **Affiliate Integration**: Direct links to vendor websites with tracking
- **Build Consultation**: Schedule consultations directly from vendor profiles

### For Admins
- **Django Admin Interface**: Manage vendors, track clicks, and view analytics
- **Geospatial Support**: PostGIS integration for location-based features
- **API-First Design**: RESTful API for all vendor operations

## Tech Stack

### Backend
- **Django 4.2** with Django REST Framework
- **PostgreSQL** with **PostGIS** for geospatial data
- **GDAL/GEOS** for geographic operations
- **django-cors-headers** for frontend integration

### Frontend
- **React** with **Vite**
- **Tailwind CSS v4** for styling
- **React Router** for navigation
- **Axios** for API communication
- **Lucide React** for icons

## Project Structure

```
gbsi/
├── core/                   # Core Django app (User model)
├── vendors/                # Vendors app (main business logic)
│   ├── models.py          # BuildingSystemVendor, AffiliateClick, ModelVendor
│   ├── views.py           # API endpoints
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # API routes
│   └── admin.py           # Django admin configuration
├── gbsi/                   # Django project settings
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   └── App.jsx        # Main app component
│   └── package.json
├── manage.py
└── create_db.py           # Database creation script
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 14+ with PostGIS extension
- GDAL and GEOS libraries

### Backend Setup

1. **Install PostgreSQL and PostGIS** (macOS):
   ```bash
   brew install postgresql postgis
   brew services start postgresql
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the database**:
   ```bash
   python create_db.py
   ```

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/api/`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173/`

## Usage

### Adding Vendors via Django Admin

1. Navigate to `http://localhost:8000/admin/`
2. Log in with your superuser credentials
3. Click on "Building System Vendors"
4. Click "Add Building System Vendor"
5. Fill in the vendor details:
   - **Partner Name**: Vendor name
   - **Website URL**: Main website
   - **Affiliate Link**: Tracked affiliate URL (e.g., `https://vendor.com/?ref=terralux`)
   - **Is Certified**: Check for certified partners
   - **Consultation Enabled**: Enable scheduling button
   - **Primary Category**: Select category
   - **Geom**: Click on map to set location

### API Endpoints

- `GET /api/vendors/` - List all vendors
- `GET /api/vendors/{id}/` - Get vendor details
- `POST /api/vendors/{id}/track_click/` - Track affiliate click

### Affiliate Tracking

When a user clicks "Visit Site" on a vendor card:
1. Frontend calls `/api/vendors/{id}/track_click/`
2. Backend creates an `AffiliateClick` record
3. User is redirected to the affiliate link
4. Analytics are available in Django admin

## Database Models

### BuildingSystemVendor
- `partner_name`: Vendor name
- `website_url`: Main website
- `affiliate_link`: Tracked affiliate URL
- `is_certified`: Certified partner badge
- `consultation_enabled`: Show scheduling button
- `geom`: Geographic location (PostGIS Point)
- `primary_category`: Category (PREFAB, NATURAL, DOMES, 3D_PRINT, etc.)
- `heal_alignment`: Sustainability rating (HIGH, MEDIUM, LOW)
- `status`: Vendor status (CORE_COUNCIL, PRIORITY, ACTIVE)
- `metadata`: JSON field for additional data
- `contact_info`: JSON field for contact details

### AffiliateClick
- `vendor`: Foreign key to BuildingSystemVendor
- `user`: Foreign key to User (nullable)
- `timestamp`: Click timestamp
- `converted`: Conversion status

## Development Notes

### Tailwind CSS v4
The frontend uses Tailwind CSS v4, which requires:
- `@tailwindcss/postcss` plugin
- `@import "tailwindcss";` in CSS instead of `@tailwind` directives

### CORS Configuration
CORS is configured to allow requests from `http://localhost:5173` and `http://127.0.0.1:5173`.

### Geospatial Configuration
GDAL and GEOS library paths are configured in `settings.py`:
```python
GDAL_LIBRARY_PATH = '/usr/local/opt/gdal/lib/libgdal.dylib'
GEOS_LIBRARY_PATH = '/usr/local/opt/geos/lib/libgeos_c.dylib'
```

Adjust these paths based on your system.

## Future Enhancements

- [ ] Cal.com integration for consultation scheduling
- [ ] AI-powered vendor ingestion from URLs/PDFs
- [ ] Advanced geospatial filtering and mapping
- [ ] Vendor analytics dashboard
- [ ] Email notifications for new consultations
- [ ] User authentication and saved vendors
- [ ] Vendor comparison tool

## License

Proprietary - TerraLux

## Contact

For questions or support, contact the TerraLux team.
