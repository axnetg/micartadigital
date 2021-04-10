from django.urls import path

from cartas import views

urlpatterns = [
    path('panel/', views.dashboard, name='panel'),
    path('establecimiento/new', views.establecimiento_create, name='new-establecimiento'),
    path('establecimiento/edit/<slug:slug>', views.establecimiento_edit, name='edit-establecimiento'),
    path('carta/new', views.CartaCreateView.as_view(), name='new-carta'),
    path('carta/edit/<int:pk>', views.carta_edit, name='edit-carta'),
    path('carta/<slug:slug>', views.establecimiento_details, name='establecimiento'),
    path('qr/<int:id>', views.establecimiento_redirect, name='redirect-establecimiento'),
    path('qrcode/<slug:slug>', views.serve_qr_code, name='serve-qr'),
]
