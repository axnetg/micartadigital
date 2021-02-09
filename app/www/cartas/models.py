from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse

class Usuario(AbstractUser):
    nif = models.CharField(max_length=9, blank=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Establecimiento(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    direccion = models.TextField(max_length=200)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    propietario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='establecimientos')
    carta = models.ForeignKey('Carta', on_delete=models.SET_NULL, null=True, blank=True, related_name='establecimientos')

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('establecimiento', kwargs={'slug': self.slug})
    

class Carta(models.Model):
    titulo = models.CharField(max_length=100)
    propietario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='cartas')

    def __str__(self):
        return self.titulo
    