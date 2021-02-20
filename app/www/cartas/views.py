from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Establecimiento


def home(request):
    establecimientos = Establecimiento.objects.all()
    return render(request, 'home.html', {'establecimientos': establecimientos})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def establecimiento_details(request, slug):
    establecimiento = get_object_or_404(Establecimiento, slug=slug)
    return render(request, 'establecimiento_details.html', {'establecimiento': establecimiento})
