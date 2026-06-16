#usar : py generar_datos.py en la terminalpara injectar datos de prueba en la base de datos MySQL (XAMPP) 
# se borraran los datos anteriores y se inyectaran 14,123 registros de fechas aleatorias
import os
import random
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colbirdProject.settings')
import django
django.setup()

from django.utils import timezone
from colbirdApp.models import Ave, Busqueda

def generar_datos_prueba():
    print("[*] Limpiando historial de búsquedas anteriores...")
    Busqueda.objects.all().delete()

    # --- MATEMÁTICAS APLICADAS PARA COHERENCIA TEMPORAL ---
    # Semana  (0-7 días): Loica 60% | Carpintero 30% | Tiuque 10%
    # Mes     (8-30 días): Se ajusta para que el total de 30 días sea Loica ~45% | Carpintero ~36% | Tiuque ~18%
    # Semestre(31-180 días): Se ajusta para que el total de 180 días sea Loica 35% | Carpintero 45% | Tiuque 20%
    # Año     (181-365 días): Se ajusta para que el total de 365 días sea Loica 45% | Carpintero 35% | Tiuque 20%
    
    tendencias = [
        # 1. Rango SEMANAL (0 a 7 días atrás) - Total: 263 búsquedas
        {'ave': 'Loica', 'cantidad': 158, 'dias_min': 0, 'dias_max': 7},
        {'ave': 'Carpintero', 'cantidad': 79, 'dias_min': 0, 'dias_max': 7},
        {'ave': 'Tiuque', 'cantidad': 26, 'dias_min': 0, 'dias_max': 7},
        
        # 2. Rango MENSUAL (8 a 30 días atrás) - Total Inyectado: 890 (Suma mensual real: 1,153)
        {'ave': 'Loica', 'cantidad': 369, 'dias_min': 8, 'dias_max': 30},
        {'ave': 'Carpintero', 'cantidad': 336, 'dias_min': 8, 'dias_max': 30},
        {'ave': 'Tiuque', 'cantidad': 185, 'dias_min': 8, 'dias_max': 30},
        
        # 3. Rango SEMESTRAL (31 a 180 días atrás) - Total Inyectado: 5,649 (Suma semestral real: 6,802)
        # Aquí el Carpintero despega para dominar el semestre
        {'ave': 'Loica', 'cantidad': 1871, 'dias_min': 31, 'dias_max': 180},
        {'ave': 'Carpintero', 'cantidad': 2639, 'dias_min': 31, 'dias_max': 180},
        {'ave': 'Tiuque', 'cantidad': 1139, 'dias_min': 31, 'dias_max': 180},

        # 4. Rango ANUAL (181 a 365 días atrás) - Total Inyectado: 7,321 (Suma anual real: 14,123)
        # Aquí la Loica recupera el trono anual
        {'ave': 'Loica', 'cantidad': 4014, 'dias_min': 181, 'dias_max': 365},
        {'ave': 'Carpintero', 'cantidad': 1843, 'dias_min': 181, 'dias_max': 365},
        {'ave': 'Tiuque', 'cantidad': 1464, 'dias_min': 181, 'dias_max': 365},
    ]

    hoy = timezone.now()
    
    nuevas_busquedas = []
    
    aves_db = {
        'Loica': Ave.objects.filter(nombreComun__icontains='Loica').first(),
        'Carpintero': Ave.objects.filter(nombreComun__icontains='Carpintero').first(),
        'Tiuque': Ave.objects.filter(nombreComun__icontains='Tiuque').first(),
    }

    print("[+] Calculando y generando 14,123 registros de fechas aleatorias. Esto tomará un segundo...")

    for tendencia in tendencias:
        ave_actual = aves_db.get(tendencia['ave'])
        
        if not ave_actual:
            print(f"[-] Error: No se encontró '{tendencia['ave']}' en la base de datos.")
            continue

        for _ in range(tendencia['cantidad']):
            dias_atras = random.randint(tendencia['dias_min'], tendencia['dias_max'])
            horas_atras = random.randint(0, 23)
            minutos_atras = random.randint(0, 59)
            segundos_atras = random.randint(0, 59)
            
            fecha_aleatoria = hoy - timedelta(
                days=dias_atras, 
                hours=horas_atras, 
                minutes=minutos_atras, 
                seconds=segundos_atras
            )
            
            nuevas_busquedas.append(
                Busqueda(ave=ave_actual, fecha=fecha_aleatoria)
            )

    print(f"[+] Inyectando datos en la base de datos MySQL (XAMPP)...")
    Busqueda.objects.bulk_create(nuevas_busquedas, batch_size=2000)

    print("\n[✔] ¡Éxito total! Las tendencias proporcionales se cargaron correctamente.")
    print("    - Ve a tu dashboard y cambia entre Semanal, Mensual, Semestral y Anual para ver la magia.")

if __name__ == '__main__':
    generar_datos_prueba()