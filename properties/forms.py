from django import forms
from .models import Property, PropertyImage, PropertyVideo

class PropertySearchForm(forms.Form):
    property_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Property.PROPERTY_TYPES,
        required=False
    )
    listing_type = forms.ChoiceField(
        choices=[('', 'All Listings')] + Property.LISTING_TYPES,
        required=False
    )
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    bedrooms = forms.IntegerField(required=False, min_value=1)
    city = forms.CharField(required=False, max_length=100)

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'listing_type', 'price',
            'address', 'city', 'state', 'zip_code', 'bedrooms', 'bathrooms',
            'square_feet', 'year_built', 'has_pool', 'has_gym', 'has_parking',
            'has_elevator', 'has_security', 'is_furnished', 'has_air_conditioning',
            'has_heating', 'main_image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_primary']

class PropertyVideoForm(forms.ModelForm):
    class Meta:
        model = PropertyVideo
        fields = ['video_url', 'title'] 