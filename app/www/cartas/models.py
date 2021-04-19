from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from multiselectfield import MultiSelectField

import uuid

from .utils import *


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return '{0}.{1}'.format(uuid.uuid4(), ext)


class Establecimiento(models.Model):
    nombre = models.CharField(verbose_name='nombre', max_length=100)
    slug = models.SlugField(verbose_name='dirección URL', unique=True)
    calle = models.CharField(verbose_name='calle', max_length=200)
    provincia = models.CharField(verbose_name='provincia', max_length=50)
    localidad = models.CharField(verbose_name='localidad', max_length=100)
    codigo_postal = models.CharField(verbose_name='código postal', max_length=5)
    telefono = models.CharField(verbose_name='teléfono', max_length=15, blank=True)
    imagen = models.ImageField(verbose_name='imagen de portada', upload_to=get_file_path, null=True, blank=True)
    propietario = models.ForeignKey(get_user_model(), verbose_name='propietario', on_delete=models.CASCADE, null=True, blank=True, related_name='establecimientos')
    carta = models.ForeignKey('Carta', verbose_name='carta', on_delete=models.SET_NULL, null=True, blank=True, related_name='establecimientos')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'establecimiento'
        verbose_name_plural = 'establecimientos'
        
    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('establecimiento', kwargs={'slug': self.slug})
    
    def display_direccion(self):
        return f'{self.calle}, {self.codigo_postal}, {self.localidad}'

    def save(self, *args, **kwargs):        
        try:
            current = Establecimiento.objects.get(id=self.id)
            if current.imagen != self.imagen:
                current.imagen.delete()
        except: pass
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)


class Carta(models.Model):
    titulo = models.CharField(verbose_name='nombre', max_length=100)
    ultima_modificacion = models.DateTimeField(verbose_name='última modificación', auto_now=True)
    propietario = models.ForeignKey(get_user_model(), verbose_name='propietario', on_delete=models.CASCADE, null=True, blank=True, related_name='cartas')

    class Meta:
        ordering = ['titulo']
        verbose_name = 'carta'
        verbose_name_plural = 'cartas'
        
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
    carta = models.ForeignKey(Carta, verbose_name='carta', on_delete=models.CASCADE, related_name='secciones')
    titulo = models.CharField(verbose_name='título', max_length=100)
    orden = models.PositiveSmallIntegerField(verbose_name='orden')
    
    class Meta:
        ordering = ['orden']
        verbose_name = 'sección'
        verbose_name_plural = 'secciones'
    
    def __str__(self):
        return self.titulo
    

class Plato(models.Model):
    seccion = models.ForeignKey(Seccion, verbose_name='sección', on_delete=models.CASCADE, related_name='platos')
    titulo = models.CharField(verbose_name='nombre', max_length=100)
    descripcion = models.CharField(verbose_name='descripción', max_length=400, blank=True)
    precio = models.DecimalField(verbose_name='precio', max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    alergenos = MultiSelectField(verbose_name='alérgenos', choices=TIPOS_ALERGENOS, blank=True)
    orden = models.PositiveSmallIntegerField(verbose_name='orden')
    
    class Meta:
        ordering = ['orden']
        verbose_name = 'plato'
        verbose_name_plural = 'platos'
    
    def display_alergenos(self):
        return ", ".join(self.alergenos)
    
    def __str__(self):
        return f'{self.titulo} [{self.precio}€]'