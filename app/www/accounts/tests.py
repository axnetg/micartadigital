from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import *
from django.core import mail
from django.test import TestCase
from django.urls import resolve, reverse

from .forms import *
from .views import *


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        
    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/registro/')
        self.assertEqual(view.func, signup)
        
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignupForm)
        
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="hidden"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="password"', 2)
        
    def test_form_has_fields(self):
        form = SignupForm()
        expected = ['email', 'first_name', 'last_name', 'password', 'confirm_password']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
        

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'email': 'test@cartas.es',
            'first_name': 'Test',
            'last_name': 'Case',
            'password': 'abcdef123456',
            'confirm_password': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.dashboard_url = reverse('panel')
        
    def test_dashboard_redirection(self):
        self.assertRedirects(self.response, self.dashboard_url)
        
    def test_signup_while_authenticated(self):
        response = self.client.get(reverse('signup'))
        self.assertRedirects(response, self.dashboard_url)
        
    def test_user_creation(self):
        self.assertTrue(get_user_model().objects.filter(first_name='Test').exists())
        
    def test_user_authentication(self):
        response = self.client.get(self.dashboard_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)
        
        
class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})
        
    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
        
    def test_dont_create_user(self):
        self.assertFalse(get_user_model().objects.exists())
        
        
class UserSettingsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username='test', email='test@cartas.es', password='123')
        
    def setUp(self):
        self.client.login(email='test@cartas.es', password='123')
        self.url = reverse('user-settings')
        self.response = self.client.get(self.url)
        
    def test_user_settings_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_user_settings_resolves_settings_view(self):
        view = resolve('/panel/cuenta/')
        self.assertEqual(view.func.view_class, UserSettingsUpdate)
    
    def test_user_settings_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'user_edit.html')
        
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    def test_contains_form(self):
        user_settings_form = self.response.context.get('user_settings_form')
        user_password_form = self.response.context.get('user_password_form')
        self.assertIsInstance(user_settings_form, UserSettingsUpdateForm)
        self.assertIsInstance(user_password_form, UserPasswordUpdateForm)
        
    def test_edit_user_info_valid_post_data(self):
        data = {
            'email': 'test@cartas.es',
            'first_name': 'Name',
            'last_name': 'Surname',
            'nif': '',
            'user_settings': True
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        self.assertTrue(get_user_model().objects.filter(first_name='Name').exists())
        
    def test_edit_user_info_empty_post_data(self):
        response = self.client.post(self.url, {'user_settings': True})
        form = response.context.get('user_settings_form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)
        
    def test_edit_user_password_valid_post_data(self):
        data = {
            'password': 'Cy$e8y@j',
            'confirm_password': 'Cy$e8y@j',
            'user_password': True
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        
    def test_edit_user_password_too_weak_post_data(self):
        data = {
            'password': '12345678',
            'confirm_password': '12345678',
            'user_password': True
        }
        response = self.client.post(self.url, data)
        form = response.context.get('user_password_form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)
        
    def test_edit_user_password_empty_post_data(self):
        response = self.client.post(self.url, {'user_password': True})
        form = response.context.get('user_password_form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)
        
    def test_delete_user_account_not_confirmed_post_data(self):
        response = self.client.post(self.url, {'user_delete': True})
        self.assertTrue(get_user_model().objects.exists())
        
    def test_delete_user_account_valid_post_data(self):
        data = {
            'user_confirm_delete': True,
            'user_delete': True
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(get_user_model().objects.exists())
        

class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)
        
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/cuentas/recuperar/')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetView)
        
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)
        
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="hidden"', 1) 
        self.assertContains(self.response, 'type="email"', 1)
        

class SuccessfulPasswordResetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username='test', email='test@cartas.es', password='123abcdef')
        
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'test@cartas.es'})
        
    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
        
    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))
        

class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@example.com'})
        
    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
        
    def test_no_password_reset_email(self):
        self.assertEqual(0, len(mail.outbox))
        

class PasswordResetMailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username='test', email='test@cartas.es', password='123abcdef')
        
    def setUp(self):
        self.response = self.client.post(reverse('password_reset'), {'email': 'test@cartas.es'})
        self.email = mail.outbox[0]
        
    def test_email_subject(self):
        self.assertIn('Solicitud de restablecimiento de contraseña', self.email.subject)
        
    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        
    def test_email_to(self):
        self.assertEqual(['test@cartas.es',], self.email.to)
        
    
class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/cuentas/recuperar/solicitado/')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetDoneView)
        

class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/cuentas/recuperar/completado')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetCompleteView)
