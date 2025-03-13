from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('search/', views.property_search, name='property_search'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
] 