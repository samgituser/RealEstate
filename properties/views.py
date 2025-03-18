from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Property, UserProfile, SavedProperty, PropertyInquiry, SearchHistory
from .forms import (
    PropertySearchForm, PropertyForm, PropertyImageForm, PropertyVideoForm,
    UserProfileForm, PropertyInquiryForm, ContactForm, CustomUserChangeForm, UserForm
)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def property_list(request):
    properties = Property.objects.filter(is_active=True).order_by('-created_at')
    
    # Save search history if user is logged in
    if request.user.is_authenticated:
        SearchHistory.objects.create(
            user=request.user,
            query=request.GET.get('q', ''),
            filters=request.GET
        )
    
    # Search and filter functionality
    search_form = PropertySearchForm(request.GET)
    if search_form.is_valid():
        property_type = search_form.cleaned_data.get('property_type')
        listing_type = search_form.cleaned_data.get('listing_type')
        min_price = search_form.cleaned_data.get('min_price')
        max_price = search_form.cleaned_data.get('max_price')
        bedrooms = search_form.cleaned_data.get('bedrooms')
        city = search_form.cleaned_data.get('city')
        
        if property_type:
            properties = properties.filter(property_type=property_type)
        if listing_type:
            properties = properties.filter(listing_type=listing_type)
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)
        if bedrooms:
            properties = properties.filter(bedrooms=bedrooms)
        if city:
            properties = properties.filter(city__icontains=city)
    
    # Pagination
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'properties': page_obj,
        'search_form': search_form,
    }
    return render(request, 'properties/property_list.html', context)

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk, is_active=True)
    context = {
        'property': property,
    }
    return render(request, 'properties/property_detail.html', context)

def property_search(request):
    query = request.GET.get('q')
    if query:
        properties = Property.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query) |
            Q(city__icontains=query)
        ).filter(is_active=True)
    else:
        properties = Property.objects.filter(is_active=True)
    
    context = {
        'properties': properties,
        'query': query,
    }
    return render(request, 'properties/property_search.html', context)

@login_required
def dashboard(request):
    context = {}
    
    if request.user.user_type == 'buyer':
        context.update({
            'saved_properties': SavedProperty.objects.filter(user=request.user),
            'inquiries': PropertyInquiry.objects.filter(user=request.user),
            'search_history': SearchHistory.objects.filter(user=request.user).order_by('-created_at')[:5],
        })
    elif request.user.user_type == 'agent':
        context.update({
            'properties': Property.objects.filter(created_by=request.user),
            'inquiries': PropertyInquiry.objects.filter(property__created_by=request.user),
        })
    
    return render(request, 'properties/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('properties:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=request.user)
        # Get or create the user profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'properties/profile.html', context)

@login_required
def save_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    SavedProperty.objects.get_or_create(user=request.user, property=property)
    return redirect('properties:property_detail', pk=pk)

@login_required
def remove_saved_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    SavedProperty.objects.filter(user=request.user, property=property).delete()
    return redirect('properties:property_detail', pk=pk)

@login_required
def submit_inquiry(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = property
            inquiry.user = request.user
            inquiry.save()
            return redirect('properties:property_detail', pk=pk)
    else:
        form = PropertyInquiryForm()
    
    return render(request, 'properties/inquiry_form.html', {
        'form': form,
        'property': property,
    })

class PropertyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('properties:property_list')

    def test_func(self):
        return self.request.user.user_type in ['agent', 'admin']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class PropertyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('properties:property_list')

    def test_func(self):
        property = self.get_object()
        return self.request.user.user_type == 'admin' or property.created_by == self.request.user

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you would typically send the email
            # For now, we'll just show a success message
            messages.success(request, 'Thank you for your message. We will get back to you soon!')
            return redirect('properties:contact')
    else:
        form = ContactForm()
    
    return render(request, 'properties/contact.html', {'form': form})

@login_required
def contact_agent(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    
    if not hasattr(property, 'agent'):
        messages.error(request, 'This property does not have an assigned agent.')
        return redirect('properties:property_detail', pk=property.id)
    
    agent = property.agent
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email to agent
            subject = f'New Property Inquiry: {property.title}'
            message = f"""
            New inquiry from {request.user.get_full_name()} ({request.user.email})
            
            Property: {property.title}
            Price: ${property.price}
            
            Message:
            {form.cleaned_data['message']}
            
            Contact Information:
            Phone: {form.cleaned_data['phone']}
            Email: {form.cleaned_data['email']}
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [agent.email],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent to the agent.')
                return redirect('properties:property_detail', pk=property.id)
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again later.')
    else:
        form = ContactForm(initial={
            'name': request.user.get_full_name(),
            'email': request.user.email,
            'phone': request.user.phone_number if hasattr(request.user, 'phone_number') else '',
        })
    
    context = {
        'property': property,
        'agent': agent,
        'form': form,
    }
    return render(request, 'properties/contact_agent.html', context)
