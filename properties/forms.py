from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Property, PropertyImage, PropertyVideo, UserProfile, PropertyInquiry

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'phone_number', 'profile_picture', 'bio')

class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['company_name', 'license_number', 'website', 'preferred_contact_method', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class PropertyInquiryForm(forms.ModelForm):
    class Meta:
        model = PropertyInquiry
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your message here...'}),
        }

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

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True) 