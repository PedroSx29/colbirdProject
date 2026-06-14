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