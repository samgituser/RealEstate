from django.db import models
from django.core.validators import MinValueValidator

class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
    ]
    
    LISTING_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    square_feet = models.PositiveIntegerField(null=True, blank=True)
    year_built = models.PositiveIntegerField(null=True, blank=True)
    
    # Amenities
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)
    has_security = models.BooleanField(default=False)
    is_furnished = models.BooleanField(default=False)
    has_air_conditioning = models.BooleanField(default=False)
    has_heating = models.BooleanField(default=False)
    
    # Media
    main_image = models.ImageField(upload_to='properties/main/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.property_type}"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties/gallery/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"

class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, related_name='videos', on_delete=models.CASCADE)
    video_url = models.URLField()
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for {self.property.title}"
