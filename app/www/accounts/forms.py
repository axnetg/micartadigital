from django import forms
from django.utils.crypto import get_random_string

from .models import Usuario


class SignupForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellidos', required=True)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = get_random_string(length=32)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserSettingsUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellidos', required=True)
    
    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'nif']
    
    
class UserPasswordUpdateForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput())
    
    class Meta:
        model = Usuario
        fields = ['password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user