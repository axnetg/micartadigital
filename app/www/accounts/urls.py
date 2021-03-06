from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('registro/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('salir/', auth_views.LogoutView.as_view(), name='logout'),
    path('panel/cuenta/', views.UserSettingsUpdate.as_view(), name='user-settings'),
    
    path('cuentas/recuperar/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    path('cuentas/recuperar/solicitado/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('cuentas/recuperar/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('cuentas/recuperar/completado',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
]
