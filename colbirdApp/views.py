from django.shortcuts import render
import librosa
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from colbirdApp.models import Ave

# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def comparar_audios_matematicamente(ruta_audio_guardado, ruta_audio_mic):
    try:
        # Cargar ambos audios (y = onda, sr = sample rate)
        y_ref, sr_ref = librosa.load(ruta_audio_guardado, duration=5.0)
        y_mic, sr_mic = librosa.load(ruta_audio_mic, duration=5.0)

        # Extraer características matemáticas (Mel-frequency cepstral coefficients)
        mfcc_ref = librosa.feature.mfcc(y=y_ref, sr=sr_ref, n_mfcc=13)
        mfcc_mic = librosa.feature.mfcc(y=y_mic, sr=sr_mic, n_mfcc=13)

        # Asegurar que tengan el mismo tamaño recortándolos al mínimo común
        min_len = min(mfcc_ref.shape[1], mfcc_mic.shape[1])
        mfcc_ref = mfcc_ref[:, :min_len]
        mfcc_mic = mfcc_mic[:, :min_len]

        # Calcular el error cuadrático medio (MSE) entre ambas matrices
        diferencia = np.mean((mfcc_ref - mfcc_mic) ** 2)
        
        # Si la diferencia matemática es muy cercana a 0, son el mismo sonido
        return diferencia
    except Exception as e:
        return float('inf')

def identificar_ave(request):
    if request.method == 'POST' and request.FILES.get('audio_mic'):
        audio_microfono = request.FILES['audio_mic']
        
        mejor_coincidencia = None
        menor_diferencia = float('inf')
        umbral_aceptacion = 500.0 # Este número deberás calibrarlo probando

        # Buscar en tu modelo
        todas_las_aves = Ave.objects.all()
        
        for ave in todas_las_aves:
            if ave.audio: # Asumiendo que agregaste un FileField llamado 'audio' a tu modelo Ave
                diferencia = comparar_audios_matematicamente(ave.audio.path, audio_microfono)
                
                if diferencia < menor_diferencia:
                    menor_diferencia = diferencia
                    mejor_coincidencia = ave

        # Si la diferencia matemática es menor al umbral, declaramos un "Match"
        if mejor_coincidencia and menor_diferencia < umbral_aceptacion:
            return JsonResponse({
                'encontrado': True, 
                'id': mejor_coincidencia.ave_id,
                'ave': mejor_coincidencia.nombreComun
            })
            
    return JsonResponse({'encontrado': False})