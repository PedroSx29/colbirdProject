from django.shortcuts import render
from colbirdApp.models import Ave

# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def obtenerLoica(request):
    loica = Ave.objects.filter(pk=1)
    data = {
        'ave': loica
    }
    return render(request, 'detalleAve.html', data)

def obtenerCarpintero(request):
    carpintero = Ave.objects.filter(pk=2)
    data = {
        'ave': carpintero
    }
    return render(request, 'detalleAve.html', data)

def obtenerTiuque(request):
    tiuque = Ave.objects.filter(pk=3)
    data = {
        'ave': tiuque
    }
    return render(request, 'detalleAve.html', data)