from django.urls import path

from cartas import views

urlpatterns = [
    path('panel/', views.dashboard, name='panel'),
    path('carta/<slug:slug>/', views.establecimiento_details, name='establecimiento'),
]
