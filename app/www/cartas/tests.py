from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from urllib.parse import quote

from .forms import *
from .models import *
from .views import *


class HomeTests(TestCase):
    def setUp(self):
        home_url = reverse('home')
        self.response = self.client.get(home_url)
        
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)
        
    def test_home_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'home.html')
        
    def test_home_view_contains_link_to_login_page(self):
        login_url = reverse('login')
        self.assertContains(self.response, f'href="{login_url}')
    
    def test_home_view_contains_link_to_register_page(self):
        register_page = reverse('signup')
        self.assertContains(self.response, f'href="{register_page}')
        

class DashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username='test', email='test@cartas.es', password='123')
        
    def setUp(self):
        self.client.login(email='test@cartas.es', password='123')
        dashboard_url = reverse('panel')
        self.response = self.client.get(dashboard_url)
        
    def test_dashboard_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_dashboard_url_resolves_dashboard_view(self):
        view = resolve('/panel/')
        self.assertEquals(view.func, dashboard)
    
    def test_dashboard_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'dashboard.html')
    
    def test_dashboard_view_contains_link_to_home(self):
        home_url = reverse('home')
        self.assertContains(self.response, f'href="{home_url}"')
        
    def test_dashboard_view_contains_link_to_search(self):
        search_url = reverse('search-establecimiento')
        self.assertContains(self.response, f'href="{search_url}"')
        
        
class LoginRequiredTests(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
    
    def test_dashboard_redirection(self):
        url = reverse('panel')
        response = self.client.get(url)
        self.assertRedirects(response, f'{self.login_url}?next={url}')
    
    def test_new_establecimiento_redirection(self):
        url = reverse('new-establecimiento')
        response = self.client.get(url)
        self.assertRedirects(response, f'{self.login_url}?next={quote(url)}')
    
    def test_edit_establecimiento_redirection(self):
        url = reverse('edit-establecimiento', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, f'{self.login_url}?next={url}')
    
    def test_delete_establecimiento_redirection(self):
        url = reverse('delete-establecimiento', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, f'{self.login_url}?next={url}')
    
    def test_new_carta_redirection(self):
        url = reverse('new-carta')
        response = self.client.get(url)
        self.assertRedirects(response, f'{self.login_url}?next={quote(url)}')
    
    def test_edit_carta_redirection(self):
        url = reverse('edit-carta', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, f'{self.login_url}?next={url}')
    
    def test_delete_carta_redirection(self):
        url = reverse('delete-carta', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, f'{self.login_url}?next={url}')
        

class EstablecimientoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Establecimiento.objects.create(nombre='Test', slug='test', calle='Calle', codigo_postal='32004', provincia='Ourense', localidad='Ourense')
    
    def setUp(self):
        self.est = Establecimiento.objects.get(slug='test')
        
    def test_establecimiento_view_success_status_code(self):
        url = reverse('establecimiento', kwargs={'slug': self.est.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def test_establecimiento_view_not_found_status_code(self):
        url = reverse('establecimiento', kwargs={'slug': 'not-found'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
    def test_qrcode_view_redirect_status_code(self):
        url = reverse('redirect-establecimiento', kwargs={'id': self.est.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('establecimiento', kwargs={'slug': self.est.slug}))
        
    def test_qrcode_view_not_found_status_code(self):
        url = reverse('redirect-establecimiento', kwargs={'id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)        
                        
    def test_establecimiento_url_resolves_establecimiento_view(self):
        view = resolve('/carta/test')
        self.assertEquals(view.func, establecimiento_details)
        
    def test_qrcode_url_resolves_redirect_view(self):
        view = resolve('/qr/1')
        self.assertEquals(view.func, establecimiento_redirect)
        
    def test_establecimiento_view_uses_correct_template(self):
        url = reverse('establecimiento', kwargs={'slug': self.est.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'establecimiento_details.html')
        
    def test_establecimiento_view_contains_link_to_google_maps(self):
        url = reverse('establecimiento', kwargs={'slug': self.est.slug})
        response = self.client.get(url)
        self.assertContains(response, 'href="https://maps.google.com/')
        
    def test_establecimiento_view_contains_link_to_tel(self):
        self.est.telefono1 = '666123456'
        self.est.save()
        
        url = reverse('establecimiento', kwargs={'slug': self.est.slug})
        response = self.client.get(url)
        self.assertContains(response, f'href="tel:{self.est.telefono1}"')
        
    def test_establecimiento_view_contains_link_to_social(self):
        self.est.social_wa = '+34666123456'
        self.est.social_ig = 'test-ig'
        self.est.social_fb = 'test-fb'
        self.est.social_tw = 'test-tw'
        self.est.save()
        
        url = reverse('establecimiento', kwargs={'slug': self.est.slug})
        response = self.client.get(url)
        self.assertContains(response, f'href="https://wa.me/{self.est.social_wa}"')
        self.assertContains(response, f'href="https://instagram.com/{self.est.social_ig}"')
        self.assertContains(response, f'href="https://facebook.com/{self.est.social_fb}"')
        self.assertContains(response, f'href="https://twitter.com/{self.est.social_tw}"')
        
    def test_establecimiento_view_contains_search_form(self):
        search_url = reverse('search-establecimiento')
        url = reverse('establecimiento', kwargs={'slug': self.est.slug})
        response = self.client.get(url)
        self.assertContains(response, f'action="{search_url}"')
        
    def test_get_absolute_url(self):
        self.assertEquals(self.est.get_absolute_url(), '/carta/test')
        
    def test_get_display_direccion(self):
        direccion = 'Calle, 32004, Ourense'
        self.assertEquals(self.est.display_direccion(), direccion)


class EstablecimientoFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='test', email='test@cartas.es', password='123')
        Establecimiento.objects.create(nombre='Test', slug='test', calle='Calle', codigo_postal='32004', provincia='Ourense', localidad='Ourense', propietario=user)
        
    def setUp(self):
        self.est = Establecimiento.objects.get(slug='test')
        self.client.login(email='test@cartas.es', password='123')
        
    def test_new_establecimiento_view_status_code(self):
        url = reverse('new-establecimiento')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def test_new_establecimiento_url_resolves_create_view(self):
        view = resolve('/panel/establecimiento/añadir')
        self.assertEquals(view.func, establecimiento_create)
        
    def test_new_establecimiento_view_uses_correct_template(self):
        url = reverse('new-establecimiento')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'establecimiento_form.html')
        
    def test_new_establecimiento_contains_form(self):
        url = reverse('new-establecimiento')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, EstablecimientoForm)
            
    def test_new_establecimiento_form_csrf(self):
        url = reverse('new-establecimiento')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
        
    def test_new_establecimiento_valid_post_data(self):
        url = reverse('new-establecimiento')
        data = {
            'nombre': 'Test Valid',
            'slug': 'test-valid',
            'calle': 'Test',
            'codigo_postal': '32004',
            'provincia': 'Ourense',
            'localidad': 'Ourense'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('panel'))
        self.assertTrue(Establecimiento.objects.filter(slug='test-valid').exists())
        
    def test_new_establecimiento_invalid_required_post_data(self):
        url = reverse('new-establecimiento')
        data = {
            'nombre': 'Test Invalid',
            'slug': 'test-invalid'
        }
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
        self.assertFalse(Establecimiento.objects.filter(slug='test-invalid').exists())
        
    def test_new_establecimiento_invalid_validation_post_data(self):
        url = reverse('new-establecimiento')
        data = {
            'nombre': 'Test Invalid',
            'slug': 'test-invalid',
            'calle': 'Test',
            'codigo_postal': '01234',
            'provincia': 'Ourense',
            'localidad': 'Ourense'
        }
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
        self.assertFalse(Establecimiento.objects.filter(slug='test-invalid').exists())
        
    def test_new_establecimiento_empty_post_data(self):
        url = reverse('new-establecimiento')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
        
    def test_edit_establecimiento_view_status_code(self):
        url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def test_edit_establecimiento_url_resolves_edit_view(self):
        view = resolve(f'/panel/establecimiento/{self.est.id}/editar')
        self.assertEquals(view.func, establecimiento_edit)
        
    def test_edit_establecimiento_view_uses_correct_template(self):
        url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'establecimiento_form.html')
        
    def test_edit_establecimiento_contains_form(self):
        url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, EstablecimientoForm)
        
    def test_edit_establecimiento_form_csrf(self):
        url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
        
    def test_edit_establecimiento_valid_post_data(self):
        url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        data = {
            'nombre': 'Test Valid Edit',
            'slug': 'test-valid',
            'calle': 'Test',
            'codigo_postal': '32004',
            'provincia': 'Ourense',
            'localidad': 'Ourense'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('panel'))
        self.assertIn('Test Valid Edit', Establecimiento.objects.get(slug='test-valid').nombre)
        
    def test_edit_establecimiento_invalid_post_data(self):
        url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        data = {
            'nombre': 'Test Invalid',
            'slug': 'test-invalid'
        }
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
        self.assertFalse(Establecimiento.objects.filter(slug='test-invalid').exists())
        
    def test_edit_establecimiento_empty_post_data(self):
        url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
        
    def test_delete_establecimiento_view_status_code(self):
        url = reverse('delete-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
    def test_delete_establecimiento_url_resolves_create_view(self):
        view = resolve(f'/panel/establecimiento/{self.est.id}/borrar')
        self.assertEquals(view.func, establecimiento_delete)
        
    def test_delete_establecimiento_empty_post_data(self):
        url = reverse('delete-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.post(url, {})
        self.assertRedirects(response, reverse('panel'))
        
    def test_delete_establecimiento_valid_post_data(self):
        url = reverse('delete-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.post(url, {'confirm_delete': True})
        self.assertRedirects(response, reverse('panel'))
        self.assertFalse(Establecimiento.objects.filter(slug='test').exists())
        
        
class EstablecimientoForbiddenTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username='test', email='test@cartas.es', password='123')
        user = get_user_model().objects.create_user(username='new-owner', email='user@example.com', password='123')
        Establecimiento.objects.create(nombre='Test', slug='test', calle='Calle', codigo_postal='32004', provincia='Ourense', localidad='Ourense', propietario=user)
    
    def setUp(self):
        self.est = Establecimiento.objects.get(slug='test')
        self.client.login(email='test@cartas.es', password='123')
    
    def test_edit_establecimiento_not_propietario_status_code(self):
        url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
    def test_delete_establecimiento_not_propietario_status_code(self):
        url = reverse('delete-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.post(url, {'confirm_delete': True})
        self.assertEquals(response.status_code, 404)
        self.assertTrue(Establecimiento.objects.filter(slug='test').exists())