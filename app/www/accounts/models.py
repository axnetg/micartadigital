from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    email = models.EmailField(verbose_name='correo electrónico', unique=True)
    nif = models.CharField(verbose_name='NIF', max_length=9, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return self.get_full_name()
