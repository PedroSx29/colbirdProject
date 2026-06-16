from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from colbirdApp.models import Ave, Busqueda

def registrar_busqueda(ave_qs):
    ave = ave_qs.first()
    if ave:
        Busqueda.objects.create(ave=ave)

def inicio(request):
    return render(request, 'index.html')

def obtenerLoica(request):
    loica = Ave.objects.filter(pk=1)
    registrar_busqueda(loica) 
    data = {
        'ave': loica
    }
    return render(request, 'detalleAve.html', data)

def obtenerCarpintero(request):
    carpintero = Ave.objects.filter(pk=2)
    registrar_busqueda(carpintero) 
    data = {
        'ave': carpintero
    }
    return render(request, 'detalleAve.html', data)

def obtenerTiuque(request):
    tiuque = Ave.objects.filter(pk=3)
    registrar_busqueda(tiuque) 
    data = {
        'ave': tiuque
    }
    return render(request, 'detalleAve.html', data)

def datos_dashboard(request):
    filtro = request.GET.get('filtro', 'semanal')
    hoy = timezone.now()
    
    if filtro == 'semanal':
        fecha_inicio = hoy - timedelta(days=7)
    elif filtro == 'mensual':
        fecha_inicio = hoy - timedelta(days=30)
    elif filtro == 'semestral':
        fecha_inicio = hoy - timedelta(days=180)
    elif filtro == 'anual':
        fecha_inicio = hoy - timedelta(days=365)
    else:
        fecha_inicio = hoy - timedelta(days=7)
    busquedas = Busqueda.objects.filter(fecha__gte=fecha_inicio)
    
    datos_agrupados = busquedas.values('ave__nombreComun').annotate(total=Count('id'))
    todas_las_aves = Ave.objects.all()
    resultados = {ave.nombreComun: 0 for ave in todas_las_aves}
    
    for d in datos_agrupados:
        resultados[d['ave__nombreComun']] = d['total']
        
    return JsonResponse({
        'labels': list(resultados.keys()),
        'data': list(resultados.values())
    })