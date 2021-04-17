from django.contrib import admin

from .models import *


@admin.register(Establecimiento)
class EstablecimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'carta', 'propietario')
    prepopulated_fields = {'slug': ('nombre',)}


class SeccionInline(admin.TabularInline):
    model = Seccion
    extra = 1
    
class PlatoInline(admin.TabularInline):
    model = Plato
    extra = 1
    
    
@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'propietario', 'ultima_modificacion')
    inlines = [SeccionInline]
    ordering = ['ultima_modificacion']
    
    
@admin.register(Seccion)
class SeccionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden', 'carta')
    inlines = [PlatoInline]
    

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'orden', 'seccion')