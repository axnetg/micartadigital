from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .forms import *
from .models import *

from nested_formset import nestedformset_factory

import qrcode


def home(request):
    establecimientos = Establecimiento.objects.all()
    return render(request, 'home.html', {'establecimientos': establecimientos})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def establecimiento_details(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    return render(request, 'establecimiento_details.html', {'establecimiento': establecimiento})


def establecimiento_redirect(request, id):
    establecimiento = get_object_or_404(Establecimiento, id=id)
    return redirect('establecimiento', establecimiento.slug)


@login_required
def establecimiento_create(request):
    if request.method == 'POST':
        form = EstablecimientoForm(request.POST, request.FILES, current_user=request.user)
        if form.is_valid():
            establecimiento = form.save(commit=False)
            establecimiento.propietario = request.user
            establecimiento.save()
            return redirect('panel')
    else:
        form = EstablecimientoForm(current_user=request.user)
    return render(request, 'establecimiento_create.html', {'form': form})


@login_required
def establecimiento_edit(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    if request.user != establecimiento.propietario:
        raise Http404('El establecimiento que intentas editar no te pertenece.')
    
    if request.method == 'POST':
        form = EstablecimientoForm(request.POST, request.FILES, instance=establecimiento, current_user=request.user)
        if form.is_valid():
            establecimiento = form.save()
            return redirect('panel')
    else:
        form = EstablecimientoForm(instance=establecimiento, current_user=request.user)
    return render(request, 'establecimiento_create.html', {'form': form})


class CartaCreateView(LoginRequiredMixin, CreateView):
    model = Carta
    fields = ['titulo']
    template_name = 'carta_create.html'
    
    def form_valid(self, form):
        form.instance.propietario = self.request.user
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('edit-carta', args=[self.object.id])
    
    
class CartaUpdateView(LoginRequiredMixin, UpdateView):
    model = Carta
    fields = '__all__'
    template_name = 'carta_edit.html'
    ordering = ['secciones.orden']
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.propietario:
            raise Http404('La carta que intentas editar no te pertenece.')
        return super().get(request, *args, **kwargs)
        
    def get_form_class(self):
        return nestedformset_factory(
            Carta, Seccion,
            nested_formset=inlineformset_factory(
                Seccion, Plato, fields='__all__', min_num=1, max_num=50, validate_min=False, extra=0
            ),
            min_num=1, max_num=20, validate_min=False, extra=0
        )
    
    def get_success_url(self):
        return reverse('panel')
    
    
def serve_qr_code(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    permalink = reverse('redirect-establecimiento', args=[establecimiento.id])
    uri = request.build_absolute_uri(permalink)
    
    response = HttpResponse(content_type="image/png")
    img = qrcode.make(uri)
    img.save(response, "PNG")
    return response