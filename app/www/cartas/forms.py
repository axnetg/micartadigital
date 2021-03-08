from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import Establecimiento, Carta
from .widgets import LabeledInput

import re
import requests


class NewEstablecimientoForm(forms.ModelForm):
    class Meta:
        model = Establecimiento
        fields = ['nombre', 'slug', 'calle', 'codigo_postal', 'provincia', 'localidad', 'telefono', 'imagen']
    
        
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)
        #self.fields['carta'].queryset = Carta.objects.filter(propietario=current_user)
        
        codigo_postal = self['codigo_postal'].value() if self.is_bound else self.instance.codigo_postal
        localidad_choices = self.get_places_by_postal_code(codigo_postal)
        
        self.fields['slug'].widget = LabeledInput(attrs={'label': 'http://localhost:8000/carta/'})
        self.fields['provincia'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['localidad'].widget = forms.Select(attrs={'class': 'ui dropdown'}, choices=localidad_choices)
        self.fields['telefono'].widget = forms.TextInput(attrs={'type': 'tel'})
    
    
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
    
    
    def valid_postal_code(self, codigo_postal):
        return re.fullmatch('^(0[1-9]|[1-4][0-9]|5[0-2])[0-9]{3}$', codigo_postal)
    
    
    def clean_codigo_postal(self):
        codigo_postal = self.cleaned_data['codigo_postal']
        if not self.valid_postal_code(codigo_postal):
            raise ValidationError('El código postal introducido es inválido')
        
        return codigo_postal
    
    
    def clean_provincia(self):
        provincia = self.cleaned_data['provincia']
        codigo_postal = self.cleaned_data.get('codigo_postal', '')
        
        if not provincia == self.get_provincia_by_postal_code(codigo_postal):
            raise ValidationError('La provincia introducida no se corresponde con el código postal.')
        
        return provincia
    
    
    def clean_localidad(self):
        localidad = self.cleaned_data['localidad']
        codigo_postal = self.cleaned_data.get('codigo_postal', '')
        
        if not any( localidad in x for x in self.get_places_by_postal_code(codigo_postal) ):
            raise ValidationError('La localidad introducida no se corresponde con el código postal.')
        
        return localidad