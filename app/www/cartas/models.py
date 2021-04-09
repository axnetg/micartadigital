from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from multiselectfield import MultiSelectField

import uuid

from .utils import *


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return '{0}/{1}.{2}'.format(instance.slug, uuid.uuid4(), ext)


class Establecimiento(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    calle = models.CharField(max_length=200)
    provincia = models.CharField(max_length=50)
    localidad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    telefono = models.CharField(max_length=15, blank=True)
    imagen = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    propietario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='establecimientos')
    carta = models.ForeignKey('Carta', on_delete=models.SET_NULL, null=True, blank=True, related_name='establecimientos')

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('establecimiento', kwargs={'slug': self.slug})
    
    def display_direccion(self):
        return f'{self.calle}, {self.localidad}, {self.codigo_postal}'

    def save(self, *args, **kwargs):        
        try:
            this = Establecimiento.objects.get(id=self.id)
            if this.imagen != self.imagen:
                this.imagen.delete()
        except:
            pass
        super().save(*args, **kwargs)


class Carta(models.Model):
    titulo = models.CharField(max_length=100)
    propietario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='cartas')

    def __str__(self):
        return self.titulo
    
    def display_establecimientos_en_uso(self):
        return ', '.join([est.nombre for est in self.establecimientos.all()])
    
    def count_platos(self):
        platos = 0
        for seccion in self.secciones.all():
            platos += seccion.platos.count()
        return platos
    
    
class Seccion(models.Model):
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE, related_name='secciones')
    titulo = models.CharField(max_length=100)
    orden = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.titulo
    

class Plato(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='platos')
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=400, blank=True)
    precio = models.FloatField()
    alergenos = MultiSelectField(choices=TIPOS_ALERGENOS, blank=True)
    orden = models.PositiveSmallIntegerField()
    
    def display_alergenos(self):
        print(self.alergenos)
            
        return ", ".join(self.alergenos)
    
    def __str__(self):
        return f'{self.titulo} [{self.precio}€]'