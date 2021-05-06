from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import *
from .widgets import LabeledInput

import re
import requests


class EstablecimientoForm(forms.ModelForm):
    class Meta:
        model = Establecimiento
        fields = ['nombre', 'slug', 'calle', 'codigo_postal',
                  'provincia', 'localidad', 'telefono1', 'telefono2',
                  'social_wa', 'social_ig', 'social_fb', 'social_tw',
                  'carta', 'imagen']
    
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        
        slug_url = f"{self.request.build_absolute_uri(reverse('home'))}carta/"
        codigo_postal = self['codigo_postal'].value() if self.is_bound else self.instance.codigo_postal
        localidad_choices = self.get_places_by_postal_code(codigo_postal)
        
        self.fields['slug'].widget = LabeledInput(attrs={'label': slug_url})
        self.fields['provincia'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['localidad'].widget = forms.Select(attrs={'class': 'ui search dropdown'}, choices=localidad_choices)
        self.fields['telefono1'].widget = forms.TextInput(attrs={'type': 'tel'})
        self.fields['telefono2'].widget = forms.TextInput(attrs={'type': 'tel'})
        self.fields['social_wa'].widget = LabeledInput(attrs={'label': 'https://wa.me/'})
        self.fields['social_ig'].widget = LabeledInput(attrs={'label': 'https://instagram.com/'})
        self.fields['social_fb'].widget = LabeledInput(attrs={'label': 'https://facebook.com/'})
        self.fields['social_tw'].widget = LabeledInput(attrs={'label': 'https://twitter.com/'})
        self.fields['carta'].widget = forms.Select(attrs={'class': 'ui search dropdown'})
        self.fields['carta'].queryset = Carta.objects.filter(propietario=self.request.user)
    
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        return nombre[0].upper() + nombre[1:]
    
    def clean_slug(self):
        return self.cleaned_data.get('slug').lower()
    
    def clean_calle(self):
        calle = self.cleaned_data.get('calle')
        return calle[0].upper() + calle[1:]
    
    def clean_codigo_postal(self):
        codigo_postal = self.cleaned_data.get('codigo_postal')
        if not self.valid_postal_code(codigo_postal):
            raise ValidationError('El código postal introducido es inválido')
        return codigo_postal
    
    def clean_provincia(self):
        provincia = self.cleaned_data.get('provincia')
        codigo_postal = self.cleaned_data.get('codigo_postal')
        
        if not provincia == self.get_provincia_by_postal_code(codigo_postal):
            raise ValidationError('La provincia introducida no se corresponde con el código postal.')
        return provincia
    
    def clean_localidad(self):
        localidad = self.cleaned_data.get('localidad')
        codigo_postal = self.cleaned_data.get('codigo_postal')
        
        if not any( localidad in x for x in self.get_places_by_postal_code(codigo_postal) ):
            raise ValidationError('La localidad introducida no se corresponde con el código postal.')
        return localidad
    
    def clean_telefono1(self):
        telefono = self.cleaned_data.get('telefono1')
        telefono = re.sub(r'[\s\(\)\/-]', '', telefono)
        
        if telefono:
            if not self.valid_phone_number(telefono):
                raise ValidationError('Formato de teléfono inválido.')
        return telefono
    
    def clean_telefono2(self):
        telefono = self.cleaned_data.get('telefono2')
        telefono = re.sub(r'[\s\(\)\/-]', '', telefono)
        
        if telefono:
            if not self.valid_phone_number(telefono):
                raise ValidationError('Formato de teléfono inválido.')
        return telefono
    
    def get_places_by_postal_code(self, codigo_postal):
        places = []
        if codigo_postal and self.valid_postal_code(codigo_postal):
            params = {'country': 'ES', 'maxRows': '100', 'postalcode': codigo_postal}
            data = requests.get('https://www.geonames.org/postalCodeLookupJSON', params=params).json()
            for place in data['postalcodes']:
                value = place['placeName']
                places.append( (value, value) )
        return places
    
    def get_provincia_by_postal_code(self, codigo_postal):
        if codigo_postal and self.valid_postal_code(codigo_postal):
            params = {'country': 'ES', 'maxRows': '1', 'postalcode': codigo_postal}
            data = requests.get('https://www.geonames.org/postalCodeLookupJSON', params=params).json()
            if data['postalcodes']:
                return data['postalcodes'][0]['adminName2']
        return None
    
    def clean(self):
        cleaned_data = super().clean()
        telefono1 = cleaned_data.get('telefono1')
        telefono2 = cleaned_data.get('telefono2')
        
        if telefono2 and not telefono1:
            cleaned_data['telefono1'] = telefono2
            cleaned_data['telefono2'] = ''
    
    def valid_phone_number(self, phone):
        return re.fullmatch('^(\+[0-9]{1,3})?[0-9]{4,14}$', phone)
    
    def valid_postal_code(self, codigo_postal):
        return re.fullmatch('^(0[1-9]|[1-4][0-9]|5[0-2])[0-9]{3}$', codigo_postal)


class CartaForm(forms.ModelForm):
    class Meta:
        model = Carta
        fields = ['titulo']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Nombre de la carta'}),
        }
        
    
class SeccionForm(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título de la sección'}),
            'orden': forms.HiddenInput(),
        }
        
    def has_changed(self):
        return super().has_changed() or self.nested.has_changed()

 
class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = '__all__'
        localized_fields = ['precio']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Nombre del plato'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripción del plato (opcional)'}),
            'precio': LabeledInput(attrs={'placeholder': 'Precio del plato', 'label': '€', 'right': True}),
            'alergenos': forms.SelectMultiple(attrs={'class': 'ui search multiple selection dropdown'}),
            'orden': forms.HiddenInput(),
        }
        error_messages = {
            'precio': {
                'max_whole_digits': 'El precio no puede superar los 9999,99€.',
                'max_digits': 'El precio no puede contener más de 6 dígitos.',
                'max_decimal_places': 'El precio contiene demasiados decimales.',
            },
        }
