from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .forms import EstablecimientoForm
from .formsets import SeccionesFormset
from .models import *
from .utils import *

import qrcode


def home(request):
    establecimientos = Establecimiento.objects.all()
    return render(request, 'home.html', {'establecimientos': establecimientos})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def establecimiento_details(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    alergenos = zip(TIPOS_ALERGENOS, DESC_ALERGENOS)
    return render(request, 'establecimiento_details.html', {'establecimiento': establecimiento, 'alergenos': alergenos})


def establecimiento_redirect(request, id):
    establecimiento = get_object_or_404(Establecimiento, id=id)
    return redirect('establecimiento', establecimiento.slug)


@login_required
def establecimiento_create(request):
    if request.method == 'POST':
        form = EstablecimientoForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            establecimiento = form.save(commit=False)
            establecimiento.propietario = request.user
            establecimiento.save()
            return redirect('panel')
    else:
        form = EstablecimientoForm(request=request)
    return render(request, 'establecimiento_edit.html', {'form': form})


@login_required
def establecimiento_edit(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    if request.user != establecimiento.propietario:
        messages.error(request, 'El establecimiento que intentas editar no te pertenece.')
        return redirect('panel')
    
    if request.method == 'POST':
        form = EstablecimientoForm(request.POST, request.FILES, instance=establecimiento, request=request)
        if form.is_valid():
            establecimiento = form.save()
            return redirect('panel')
    else:
        form = EstablecimientoForm(instance=establecimiento, request=request)
    return render(request, 'establecimiento_edit.html', {'form': form})


class CartaCreateView(LoginRequiredMixin, CreateView):
    model = Carta
    fields = ['titulo']
    template_name = 'carta_create.html'
    
    def form_valid(self, form):
        form.instance.propietario = self.request.user
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('edit-carta', args=[self.object.id])


@login_required
def carta_edit(request, pk):
    carta = get_object_or_404(Carta, pk=pk)
    if request.user != carta.propietario:
        messages.error(request, 'La carta que intentas editar no te pertenece.')
        return redirect('panel')
    
    if request.method == 'POST':
        formset = SeccionesFormset(request.POST, instance=carta)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Los cambios realizados se han guardado correctamente')
            if 'save-and-exit' in request.POST:
                return redirect('panel')
            else:
                return redirect('edit-carta', carta.pk)
            
        messages.error(request, 'Los cambios no se han guardado. Revisa el formulario.')
    else:
        formset = SeccionesFormset(instance=carta)
        
    return render(request, 'carta_edit.html', {'carta': carta, 'form': formset})
    
    
def serve_qr_code(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    permalink = reverse('redirect-establecimiento', args=[establecimiento.id])
    uri = request.build_absolute_uri(permalink)
    
    response = HttpResponse(content_type="image/png")
    img = qrcode.make(uri)
    img.save(response, "PNG")
    return response