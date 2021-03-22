from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import NewEstablecimientoForm
from .models import Establecimiento

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
        form = NewEstablecimientoForm(request.POST, request.FILES, current_user=request.user)
        if form.is_valid():
            establecimiento = form.save(commit=False)
            establecimiento.propietario = request.user
            establecimiento.save()
            return redirect('panel')
    else:
        form = NewEstablecimientoForm(current_user=request.user)
    return render(request, 'establecimiento_create.html', {'form': form})


@login_required
def establecimiento_edit(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    if request.user != establecimiento.propietario:
        raise Http404('El establecimiento que intentas editar no te pertenece.')
    
    if request.method == 'POST':
        form = NewEstablecimientoForm(request.POST, request.FILES, instance=establecimiento, current_user=request.user)
        if form.is_valid():
            establecimiento = form.save()
            return redirect('panel')
    else:
        form = NewEstablecimientoForm(instance=establecimiento, current_user=request.user)
    return render(request, 'establecimiento_create.html', {'form': form})


def serve_qr_code(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    permalink = reverse('redirect-establecimiento', args=[establecimiento.id])
    uri = request.build_absolute_uri(permalink)
    
    response = HttpResponse(content_type="image/png")
    img = qrcode.make(uri)
    img.save(response, "PNG")
    return response