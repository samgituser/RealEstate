from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    # Property views
    path('', views.property_list, name='property_list'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('search/', views.property_search, name='property_search'),
    
    # User views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Property interactions
    path('save/<int:pk>/', views.save_property, name='add_to_saved'),
    path('remove-saved/<int:pk>/', views.remove_saved_property, name='remove_from_saved'),
    path('inquiry/<int:pk>/', views.submit_inquiry, name='submit_inquiry'),
    path('contact/<int:property_id>/', views.contact_agent, name='contact_agent'),
    
    # Property management
    path('create/', views.PropertyCreateView.as_view(), name='property_create'),
    path('update/<int:pk>/', views.PropertyUpdateView.as_view(), name='property_update'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
] 