from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='panel'),
    path('establecimiento/añadir', views.establecimiento_create, name='new-establecimiento'),
    path('establecimiento/<int:pk>/editar', views.establecimiento_edit, name='edit-establecimiento'),
    path('establecimiento/<int:pk>/borrar', views.establecimiento_delete, name='delete-establecimiento'),
    path('carta/añadir', views.carta_create, name='new-carta'),
    path('carta/<int:pk>/editar', views.carta_edit, name='edit-carta'),
    path('carta/<int:pk>/borrar', views.carta_delete, name='delete-carta'),
    path('qrcode/<slug:slug>', views.serve_qr_code, name='serve-qr'),
]
