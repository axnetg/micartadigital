from django import forms
from django.contrib.auth import password_validation
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe

from .models import Usuario


class SignupForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellidos', required=True)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'password']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return email

        raise forms.ValidationError(mark_safe('Ya existe una cuenta con este correo electrónico. Si es el tuyo, <a href="/login/">inicia sesión</a>.'))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password', error)

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
        widgets = {
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        
    def clean_email(self):
        return self.instance.email
    
    
class UserPasswordUpdateForm(forms.ModelForm):
    password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput())
    
    class Meta:
        model = Usuario
        fields = ['password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')
    
    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password', error)
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user