from django.contrib import admin
from .models import Property, PropertyImage, PropertyVideo

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'listing_type', 'price', 'city', 'bedrooms', 'is_active')
    list_filter = ('property_type', 'listing_type', 'is_active', 'city', 'bedrooms')
    search_fields = ('title', 'description', 'address', 'city', 'state')
    inlines = [PropertyImageInline, PropertyVideoInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'property_type', 'listing_type', 'price')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'square_feet', 'year_built')
        }),
        ('Amenities', {
            'fields': (
                'has_pool', 'has_gym', 'has_parking', 'has_elevator',
                'has_security', 'is_furnished', 'has_air_conditioning', 'has_heating'
            )
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
