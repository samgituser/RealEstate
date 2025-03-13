# Real Estate Website

A professional real estate website built with Django that allows users to browse, search, and view property listings.

## Features

- Property listing system with detailed information
- Advanced search and filtering options
- Image galleries and virtual tours
- Responsive design with Bootstrap 5
- Admin interface for property management

## Requirements

- Python 3.8 or higher
- Django 5.0 or higher
- Pillow (for image processing)
- django-crispy-forms
- crispy-bootstrap5

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd real-estate
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install django pillow django-crispy-forms crispy-bootstrap5
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/ in your web browser.

## Admin Interface

Access the admin interface at http://127.0.0.1:8000/admin/ using your superuser credentials to:
- Add, edit, and remove property listings
- Manage property images and virtual tours
- Update property details and amenities

## Project Structure

- `properties/` - Main application directory
  - `models.py` - Database models for properties
  - `views.py` - View functions for handling requests
  - `urls.py` - URL routing configuration
  - `forms.py` - Forms for property search and management
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JavaScript, images)
  - `media/` - User-uploaded files

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 