from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib import messages
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import EstablecimientoForm, CartaForm
from .formsets import SeccionesFormset
from .models import *
from .utils import *

import qrcode
import re


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
            messages.success(request, f'El establecimiento \'{establecimiento.nombre}\' se ha registrado con éxito.')
            return redirect('panel')
    else:
        form = EstablecimientoForm(request=request)
    return render(request, 'establecimiento_form.html', {'form': form})


@login_required
def establecimiento_edit(request, pk):
    establecimiento = get_object_or_404(Establecimiento, pk=pk)
    if request.user != establecimiento.propietario:
        messages.error(request, 'El establecimiento que intentas editar no te pertenece.')
        return redirect('panel')
    
    if request.method == 'POST':
        if 'imagen-clear' in request.POST:
            establecimiento.imagen.delete()
        if 'imagen' in request.FILES:
            if 'image' in request.FILES['imagen'].content_type:
                establecimiento.imagen = request.FILES['imagen']
                establecimiento.save()
        
        form = EstablecimientoForm(request.POST, instance=establecimiento, request=request)
        if form.is_valid():
            establecimiento = form.save()
            if 'imagen' in request.FILES and not 'image' in request.FILES['imagen'].content_type:
                form.add_error('imagen', 'Envía una imagen válida. El fichero que has enviado no era una imagen o se trataba de una imagen corrupta.')
            else:
                messages.success(request, f'El establecimiento \'{establecimiento.nombre}\' se ha modificado con éxito.')
                return redirect('panel')
    else:
        form = EstablecimientoForm(instance=establecimiento, request=request)
    return render(request, 'establecimiento_form.html', {'form': form})


@login_required
def establecimiento_delete(request, pk):
    if request.method == 'POST':
        establecimiento = get_object_or_404(Establecimiento, pk=pk)
        if request.user != establecimiento.propietario:
            messages.error(request, 'El establecimiento que intentas eliminar no te pertenece.')
            return redirect('panel')
        else:
            if 'confirm_delete' in request.POST:
                establecimiento.delete()
                messages.success(request, f'El establecimiento \'{establecimiento.nombre}\' ha sido eliminado con éxito.')
            else:
                messages.error(request, f'Ha ocurrido un problema al intentar eliminar el establecimiento \'{establecimiento.nombre}\'.')
            return redirect('panel')
    raise Http404()


def establecimiento_search(request):
    query = request.GET.get('q', '')
    query = re.sub(r'[.,\/#!?$%\^&\*;:{}=\-_`~()]', '', query)
    search_list = query.split()
    
    establecimientos = Establecimiento.objects.filter(codigo_postal__exact=query)        
    if not establecimientos.exists():
        establecimientos = Establecimiento.objects.annotate(
            #similarity=sum([ TrigramSimilarity('nombre', x) + TrigramSimilarity('calle', x) + TrigramSimilarity('localidad', x) for x in search_list ])
            similarity=TrigramSimilarity('nombre', query) + TrigramSimilarity('calle', query) + TrigramSimilarity('localidad', query)
        ).filter(similarity__gte=0.25).order_by('-similarity')
        #.exclude(carta__isnull=True)   #.order_by(F('imagen').desc(nulls_last=True))
    
    localidades = establecimientos.values('localidad').annotate(count=Count('localidad')).order_by('-count')
    context = {
        'query': query,
        'establecimientos': establecimientos,
        'localidades': localidades,
    }
    
    return render(request, 'establecimiento_search.html', context)

@login_required
def carta_create(request):
    if request.method == 'POST':
        form_carta = CartaForm(request.POST)
        formset = SeccionesFormset(request.POST)
        
        if form_carta.is_valid() and formset.is_valid():
            carta = form_carta.save(commit=False)
            carta.propietario = request.user
            carta.save()
            
            formset.instance = carta
            formset.save()
            
            messages.success(request, 'Los cambios realizados se han guardado correctamente')
            if 'save-and-exit' in request.POST:
                return redirect('panel')
            else:
                return redirect('edit-carta', carta.id)
            
        messages.error(request, 'Los cambios no se han guardado. Revisa el formulario.')
    else:
        form_carta = CartaForm()
        formset = SeccionesFormset()
        
    return render(request, 'carta_form.html', {'carta': form_carta, 'form': formset})


@login_required
def carta_edit(request, pk):
    carta = get_object_or_404(Carta, pk=pk)
    if request.user != carta.propietario:
        messages.error(request, 'La carta que intentas editar no te pertenece.')
        return redirect('panel')
    
    if request.method == 'POST':
        form_carta = CartaForm(request.POST, instance=carta)
        formset = SeccionesFormset(request.POST, instance=carta)
        
        if form_carta.is_valid() and formset.is_valid():
            form_carta.save()
            formset.save()
            
            messages.success(request, 'Los cambios realizados se han guardado correctamente')
            if 'save-and-exit' in request.POST:
                return redirect('panel')
            else:
                return redirect('edit-carta', carta.id)
            
        messages.error(request, 'Los cambios no se han guardado. Revisa el formulario.')
    else:
        form_carta = CartaForm(instance=carta)
        formset = SeccionesFormset(instance=carta)
        
    return render(request, 'carta_form.html', {'carta': form_carta, 'form': formset})


@login_required
def carta_delete(request, pk):
    if request.method == 'POST':
        carta = get_object_or_404(Carta, pk=pk)
        if request.user != carta.propietario:
            messages.error(request, 'La carta que intentas eliminar no te pertenece.')
            return redirect('panel')
        else:
            if 'confirm_delete' in request.POST:
                carta.delete()
                messages.success(request, f'La carta \'{carta.titulo}\' ha sido eliminada con éxito.')
            else:
                messages.error(request, f'Ha ocurrido un problema al intentar eliminar la carta \'{carta.titulo}\' .')
            return redirect('panel')
    raise Http404()

    
def serve_qr_code(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    permalink = reverse('redirect-establecimiento', args=[establecimiento.id])
    uri = request.build_absolute_uri(permalink)
    
    response = HttpResponse(content_type="image/png")
    img = qrcode.make(uri)
    img.save(response, "PNG")
    return response