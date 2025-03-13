from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Property
from .forms import PropertySearchForm

# Create your views here.

def property_list(request):
    properties = Property.objects.filter(is_active=True).order_by('-created_at')
    
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
    paginator = Paginator(properties, 12)  # Show 12 properties per page
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
