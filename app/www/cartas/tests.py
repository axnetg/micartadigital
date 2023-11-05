from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from urllib.parse import quote

from .forms import *
from .formsets import *
from .models import *
from .views import *


class HomeTests(TestCase):
    def setUp(self):
        home_url = reverse('home')
        self.response = self.client.get(home_url)
        
    def test_home_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)
        
    def test_home_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'home.html')
        
    def test_home_view_contains_link_to_login_page(self):
        login_url = reverse('login')
        self.assertContains(self.response, f'href="{login_url}')
    
    def test_home_view_contains_link_to_register_page(self):
        register_page = reverse('signup')
        self.assertContains(self.response, f'href="{register_page}')
        
    def test_home_view_contains_search_form(self):
        search_url = reverse('search-establecimiento')
        self.assertContains(self.response, f'action="{search_url}"')
        

class DashboardBaseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username='test', email='test@cartas.es', password='123')
        
    def setUp(self):
        self.client.login(email='test@cartas.es', password='123')
        self.response = self.client.get(reverse('panel'))
        
    def test_dashboard_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_dashboard_url_resolves_dashboard_view(self):
        view = resolve('/panel/')
        self.assertEqual(view.func, dashboard)
    
    def test_dashboard_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'dashboard.html')
    
    def test_dashboard_view_contains_link_to_home(self):
        home_url = reverse('home')
        self.assertContains(self.response, f'href="{home_url}"')
        
    def test_dashboard_view_contains_link_to_search(self):
        search_url = reverse('search-establecimiento')
        self.assertContains(self.response, f'href="{search_url}"')
        
    def test_dashboard_view_contains_link_to_user_settings(self):
        settings_url = reverse('user-settings')
        self.assertContains(self.response, f'href="{settings_url}"')
        
    def test_dashboard_view_contains_link_to_logout(self):
        logout_url = reverse('logout')
        self.assertContains(self.response, f'href="{logout_url}"')
        
    def test_dashboard_view_contains_link_to_new_establecimiento(self):
        new_establecimiento_url = reverse('new-establecimiento')
        self.assertContains(self.response, f'href="{new_establecimiento_url}"')
        
    def test_dashboard_view_contains_link_to_new_carta(self):
        new_carta_url = reverse('new-carta')
        self.assertContains(self.response, f'href="{new_carta_url}"')
        
    def test_dashboard_view_no_establecimientos(self):
        user = self.response.context.get('user')
        self.assertContains(self.response, 'Todavía no has creado establecimientos')
        self.assertFalse(user.establecimientos.exists())
        
    def test_dashboard_view_no_cartas(self):
        user = self.response.context.get('user')
        self.assertContains(self.response, 'Todavía no has creado cartas')
        self.assertFalse(user.cartas.exists())
        
        
class DashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='test', email='test@cartas.es', password='123')
        Establecimiento.objects.create(nombre='Test', slug='test', calle='Calle', codigo_postal='32004', provincia='Ourense', localidad='Ourense', propietario=user)
        Carta.objects.create(titulo='Carta Test', propietario=user)
        
    def setUp(self):
        self.client.login(email='test@cartas.es', password='123')
        self.est = Establecimiento.objects.get(slug='test')
        self.carta = Carta.objects.get(titulo='Carta Test')
        self.response = self.client.get(reverse('panel'))
        
    def test_dashboard_view_list_establecimientos(self):
        user = self.response.context.get('user')
        self.assertTrue(user.establecimientos.exists())
        self.assertQuerysetEqual(user.establecimientos.all(), [self.est])
        
    def test_dashboard_view_contains_info_establecimientos(self):
        self.assertContains(self.response, self.est.nombre)
        self.assertContains(self.response, self.est.display_direccion())
        self.assertContains(self.response, self.est.display_telefonos())
        self.assertContains(self.response, self.est.provincia)
        self.assertContains(self.response, self.est.slug)
        
    def test_dashboard_view_contains_link_to_details_establecimiento(self):
        details_url = reverse('establecimiento', kwargs={'slug': self.est.slug})
        self.assertContains(self.response, f'href="{details_url}"')
        
    def test_dashboard_view_contains_link_to_edit_establecimiento(self):
        edit_url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        self.assertContains(self.response, f'href="{edit_url}"')
        
    def test_dashboard_view_contains_link_to_serve_qr(self):
        serve_qr_url = reverse('serve-qr', kwargs={'slug': self.est.slug})
        self.assertContains(self.response, f'href="{serve_qr_url}"')
        
    def test_dashboard_view_contains_link_to_delete_establecimiento(self):
        delete_url = reverse('delete-establecimiento', kwargs={'pk': self.est.id})
        self.assertContains(self.response, f'data-url="{delete_url}"')
        
    def test_dashboard_view_list_cartas(self):
        user = self.response.context.get('user')
        self.assertTrue(user.cartas.exists())
        self.assertQuerysetEqual(user.cartas.all(), [self.carta])
        
    def test_dashboard_view_contains_info_cartas(self):
        self.assertContains(self.response, self.carta.titulo)
        self.assertContains(self.response, int(self.carta.ultima_modificacion.timestamp()))
        
    def test_dashboard_view_contains_link_to_edit_carta(self):
        edit_url = reverse('edit-carta', kwargs={'pk': self.carta.id})
        self.assertContains(self.response, f'href="{edit_url}"')
        
    def test_dashboard_view_contains_link_to_delete_carta(self):
        delete_url = reverse('delete-carta', kwargs={'pk': self.carta.id})
        self.assertContains(self.response, f'data-url="{delete_url}"')
        
        
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
        self.assertEqual(response.status_code, 200)
        
    def test_establecimiento_view_not_found_status_code(self):
        url = reverse('establecimiento', kwargs={'slug': 'not-found'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_qrcode_view_redirect_status_code(self):
        url = reverse('redirect-establecimiento', kwargs={'id': self.est.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('establecimiento', kwargs={'slug': self.est.slug}))
        
    def test_qrcode_view_not_found_status_code(self):
        url = reverse('redirect-establecimiento', kwargs={'id': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)        
                        
    def test_establecimiento_url_resolves_establecimiento_view(self):
        view = resolve('/carta/test')
        self.assertEqual(view.func, establecimiento_details)
        
    def test_qrcode_url_resolves_redirect_view(self):
        view = resolve('/qr/1')
        self.assertEqual(view.func, establecimiento_redirect)
        
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
        self.assertEqual(self.est.get_absolute_url(), '/carta/test')
        
    def test_get_display_direccion(self):
        direccion = 'Calle, 32004, Ourense'
        self.assertEqual(self.est.display_direccion(), direccion)


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
        self.assertEqual(response.status_code, 200)
        
    def test_new_establecimiento_url_resolves_create_view(self):
        view = resolve('/panel/establecimiento/añadir')
        self.assertEqual(view.func, establecimiento_create)
        
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
        self.assertEqual(response.status_code, 200)
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
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)
        self.assertFalse(Establecimiento.objects.filter(slug='test-invalid').exists())

    def test_new_establecimiento_empty_post_data(self):
        url = reverse('new-establecimiento')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)
        
    def test_edit_establecimiento_view_status_code(self):
        url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_edit_establecimiento_url_resolves_edit_view(self):
        view = resolve(f'/panel/establecimiento/{self.est.id}/editar')
        self.assertEqual(view.func, establecimiento_edit)
        
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
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)
        self.assertFalse(Establecimiento.objects.filter(slug='test-invalid').exists())
        
    def test_edit_establecimiento_empty_post_data(self):
        url = reverse('edit-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)
        
    def test_delete_establecimiento_view_status_code(self):
        url = reverse('delete-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_delete_establecimiento_url_resolves_delete_view(self):
        view = resolve(f'/panel/establecimiento/{self.est.id}/borrar')
        self.assertEqual(view.func, establecimiento_delete)
        
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
        self.assertEqual(response.status_code, 404)
        
    def test_delete_establecimiento_not_propietario_status_code(self):
        url = reverse('delete-establecimiento', kwargs={'pk': self.est.id})
        response = self.client.post(url, {'confirm_delete': True})
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Establecimiento.objects.filter(slug='test').exists())
        
        
class EstablecimientoSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Establecimiento.objects.create(nombre='Líbano Snack', slug='libano', calle='Calle Doctor Temes, 18', codigo_postal='32004', provincia='Ourense', localidad='Ourense')
        Establecimiento.objects.create(nombre='Graduado', slug='graduado', calle='Rúa Doutor Temes Fernández', codigo_postal='32004', provincia='Ourense', localidad='Ourense')
        Establecimiento.objects.create(nombre='Rebusca 46', slug='rebusca', calle='C/ Dr. Temes, nº 16B', codigo_postal='32004', provincia='Ourense', localidad='Ourense')
        Establecimiento.objects.create(nombre='Perla 3', slug='perla', calle='Rúa Carlos Velo, 1', codigo_postal='32003', provincia='Ourense', localidad='Ourense')
        Establecimiento.objects.create(nombre='Cafetería Reca', slug='reca', calle='Av. de Balaídos, 72', codigo_postal='36210', provincia='Pontevedra', localidad='Vigo')
        
    def setUp(self):
        self.url = reverse('search-establecimiento')
        
    def test_search_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_search_url_resolves_search_view(self):
        view = resolve('/buscar/')
        self.assertEqual(view.func, establecimiento_search)
        
    def test_search_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'establecimiento_search.html')
        
    def test_search_view_contains_link_to_home(self):
        response = self.client.get(self.url)
        home_url = reverse('home')
        self.assertContains(response, f'href="{home_url}"')
        
    def test_search_establecimiento_by_nombre_parcial(self):
        response = self.client.get(self.url, {'q': 'perla'})
        resultados = response.context.get('establecimientos')
        self.assertEqual(len(resultados), 1)
        
    def test_search_establecimiento_by_nombre_similar(self):
        response = self.client.get(self.url, {'q': 'cafetaria reka'})
        resultados = response.context.get('establecimientos')
        self.assertEqual(len(resultados), 1)
        
    def test_search_establecimiento_by_nombre_exacto(self):
        response = self.client.get(self.url, {'q': 'graduado'})
        resultados = response.context.get('establecimientos')
        self.assertEqual(len(resultados), 1)
        
    def test_search_establecimiento_by_calle_similar(self):
        response = self.client.get(self.url, {'q': 'avenida balaidos'})
        resultados = response.context.get('establecimientos')
        self.assertEqual(len(resultados), 1)
        
    def test_search_establecimiento_by_calle_multiple(self):
        response = self.client.get(self.url, {'q': 'doctor temes'})
        resultados = response.context.get('establecimientos')
        self.assertEqual(len(resultados), 3)
        
    def test_search_establecimiento_by_localidad_similar(self):
        response = self.client.get(self.url, {'q': 'orense'})
        resultados = response.context.get('establecimientos')
        self.assertEqual(len(resultados), 4)
        
    def test_search_establecimiento_by_calle_exacto(self):
        response = self.client.get(self.url, {'q': 'vigo'})
        resultados = response.context.get('establecimientos')
        self.assertEqual(len(resultados), 1)
        
    def test_search_establecimiento_by_codigo_postal(self):
        response = self.client.get(self.url, {'q': '32004'})
        resultados = response.context.get('establecimientos')
        self.assertEqual(len(resultados), 3)
        
        
class CartaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        carta = Carta.objects.create(titulo='Test')
        for i in range(10):
            seccion = Seccion.objects.create(titulo=f'Sección {i}', orden=i, carta=carta)
            for j in range(5):
                Plato.objects.create(titulo=f'Plato {i}-{j}', precio=j+1, orden=j, seccion=seccion)
        
        Establecimiento.objects.create(nombre='Test', slug='test', calle='Calle', codigo_postal='32004', provincia='Ourense', localidad='Ourense', carta=carta)
        
    def setUp(self):
        self.est = Establecimiento.objects.get(slug='test')
        self.response = self.client.get(reverse('establecimiento', kwargs={'slug': self.est.slug}))
        
    def test_establecimiento_contains_info_carta(self):
        secciones = self.response.context.get('establecimiento').carta.secciones.all()
        self.assertEqual(len(secciones), 10)
        for seccion in secciones:
            self.assertEqual(len(seccion.platos.all()), 5)
            
    def test_establecimiento_contains_info_titulo(self):
        for i in range(10):
            self.assertContains(self.response, f'Sección {i}')
            for j in range(5):
                self.assertContains(self.response, f'Plato {i}-{j}')
                
    def test_establecimiento_contains_info_plato(self):
        secciones = self.est.carta.secciones.all()
        for plato in [plato for seccion in secciones for plato in seccion.platos.all()]:
            self.assertContains(self.response, str(plato.precio).replace('.', ','))
            self.assertContains(self.response, plato.descripcion)
            

class CartaFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='test', email='test@cartas.es', password='123')
        carta = Carta.objects.create(titulo='Test', propietario=user)
        for i in range(10):
            seccion = Seccion.objects.create(titulo=f'Sección {i}', orden=i, carta=carta)
            for j in range(5):
                Plato.objects.create(titulo=f'Plato {i}-{j}', precio=j+1, orden=j, seccion=seccion)
                
        Establecimiento.objects.create(nombre='Test', slug='test', calle='Calle', codigo_postal='32004', provincia='Ourense', localidad='Ourense', propietario=user, carta=carta)
        
    def setUp(self):
        self.carta = Establecimiento.objects.get(slug='test').carta
        self.client.login(email='test@cartas.es', password='123')
        
    def test_new_carta_view_status_code(self):
        url = reverse('new-carta')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_new_carta_url_resolves_create_view(self):
        view = resolve('/panel/carta/añadir')
        self.assertEqual(view.func, carta_create)
        
    def test_new_carta_view_uses_correct_template(self):
        url = reverse('new-carta')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'carta_form.html')
        
    def test_new_carta_contains_form(self):
        url = reverse('new-carta')
        response = self.client.get(url)
        form_carta = response.context.get('carta')
        formset = response.context.get('form')
        self.assertIsInstance(form_carta, CartaForm)
        self.assertIsInstance(formset, SeccionFormFormSet)
        
    def test_new_carta_form_csrf(self):
        url = reverse('new-carta')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
        
    def test_new_carta_valid_post_data(self):
        url = reverse('new-carta')
        data = {
            'titulo': 'Test Carta Valid',
            'secciones-TOTAL_FORMS': 1,
            'secciones-INITIAL_FORMS': 0,
            'secciones-0-titulo': 'Secc Valid',
            'secciones-0-orden': 1,
            'secciones-0-platos-TOTAL_FORMS': 1,
            'secciones-0-platos-INITIAL_FORMS': 0,
            'secciones-0-platos-0-titulo': 'Plato Valid',
            'secciones-0-platos-0-precio': 1.00,
            'secciones-0-platos-0-orden': 1,
            'save-and-exit': True
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('panel'))
        self.assertTrue(Carta.objects.filter(titulo='Test Carta Valid').exists())
        self.assertTrue(Seccion.objects.filter(titulo='Secc Valid').exists())
        self.assertTrue(Plato.objects.filter(titulo='Plato Valid').exists())
        
    def test_new_carta_invalid_secciones_formset_post_data(self):
        url = reverse('new-carta')
        data = {
            'titulo': 'Test Carta Invalid',
            'secciones-TOTAL_FORMS': 0,
            'secciones-INITIAL_FORMS': 0
        }
        response = self.client.post(url, data)
        formset = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(formset.is_valid())
        
    def test_new_carta_invalid_platos_nested_formset_post_data(self):
        url = reverse('new-carta')
        data = {
            'titulo': 'Test Carta Valid',
            'secciones-TOTAL_FORMS': 1,
            'secciones-INITIAL_FORMS': 0,
            'secciones-0-titulo': 'Secc Valid',
            'secciones-0-orden': 1,
            'secciones-0-platos-TOTAL_FORMS': 0,
            'secciones-0-platos-INITIAL_FORMS': 0
        }
        response = self.client.post(url, data)
        formset = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(formset.errors)
        
    def test_new_establecimiento_empty_post_data(self):
        url = reverse('new-carta')
        response = self.client.post(url, {})
        carta_form = response.context.get('carta')
        formset = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(carta_form.errors)
        self.assertFalse(formset.is_valid())
        
    def test_edit_carta_view_status_code(self):
        url = reverse('edit-carta', kwargs={'pk': self.carta.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_edit_carta_url_resolves_edit_view(self):
        view = resolve(f'/panel/carta/{self.carta.id}/editar')
        self.assertEqual(view.func, carta_edit)
    
    def test_edit_carta_view_uses_correct_template(self):
        url = reverse('edit-carta', kwargs={'pk': self.carta.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'carta_form.html')
        
    def test_edit_carta_contains_form(self):
        url = reverse('edit-carta', kwargs={'pk': self.carta.id})
        response = self.client.get(url)
        form_carta = response.context.get('carta')
        formset = response.context.get('form')
        self.assertIsInstance(form_carta, CartaForm)
        self.assertIsInstance(formset, SeccionFormFormSet)
        
    def test_edit_carta_form_csrf(self):
        url = reverse('edit-carta', kwargs={'pk': self.carta.id})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_delete_carta_view_status_code(self):
        url = reverse('delete-carta', kwargs={'pk': self.carta.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_carta_url_resolves_delete_view(self):
        view = resolve(f'/panel/carta/{self.carta.id}/borrar')
        self.assertEqual(view.func, carta_delete)
    
    def test_delete_carta_empty_post_data(self):
        url = reverse('delete-carta', kwargs={'pk': self.carta.id})
        response = self.client.post(url, {})
        self.assertRedirects(response, reverse('panel'))
        
    def test_delete_carta_valid_post_data(self):
        url = reverse('delete-carta', kwargs={'pk': self.carta.id})
        response = self.client.post(url, {'confirm_delete': True})
        self.assertRedirects(response, reverse('panel'))
        self.assertFalse(Carta.objects.filter(titulo='Test').exists())
