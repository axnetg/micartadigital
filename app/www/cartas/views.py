from django.shortcuts import render, get_object_or_404

from .models import Establecimiento

def home(request):
    establecimientos = Establecimiento.objects.all()
    return render(request, 'home.html', {'establecimientos': establecimientos})

def establecimiento_details(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    return render(request, 'establecimiento_details.html', {'establecimiento': establecimiento})