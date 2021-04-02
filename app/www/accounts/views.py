from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login as auth_login
from django.views.generic import View
from django.shortcuts import render, redirect

from .forms import *


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('panel')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


class UserSettingsUpdate(LoginRequiredMixin, View):
    template_name = 'user_edit.html'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        if 'user_settings_form' not in kwargs:
            kwargs['user_settings_form'] = UserSettingsUpdateForm(instance=self.get_object())
        if 'user_password_form' not in kwargs:
            kwargs['user_password_form'] = UserPasswordUpdateForm()
            
        return kwargs
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        context = {}
        
        if 'user_settings' in request.POST:
            user_settings_form = UserSettingsUpdateForm(request.POST, instance=self.get_object())
            print(request.user.id)
            if user_settings_form.is_valid():
                user_settings_form.save()
                return redirect('user-settings')
            else:
                context['user_settings_form'] = user_settings_form
            
        elif 'user_password' in request.POST:
            user_password_form = UserPasswordUpdateForm(request.POST, instance=self.get_object())
            
            if user_password_form.is_valid():
                user = user_password_form.save()
                auth_login(request, user)
                return redirect('user-settings')
            else:
                context['user_password_form'] = user_password_form
        
        return render(request, self.template_name, self.get_context_data(**context))