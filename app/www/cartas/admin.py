from django.contrib import admin

from .models import *


@admin.register(Establecimiento)
class EstablecimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'propietario')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'propietario')
