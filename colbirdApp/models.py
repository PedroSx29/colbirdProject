from django.db import models
from django.utils import timezone

# Create your models here.
class Ave(models.Model):
    ave_id = models.AutoField(primary_key=True)
    nombreComun = models.CharField(max_length=60)
    nombreCientifico = models.CharField(max_length=60)
    familia = models.CharField(max_length=40)
    especie = models.CharField(max_length=40)
    imagen = models.FileField(upload_to='imgs_ave/', null=False, default='')
    audio = models.FileField(upload_to='audios_ave/', null=False)

    def __str__(self):
        return self.nombreComun

class Busqueda(models.Model):
    ave = models.ForeignKey(Ave, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Búsqueda: {self.ave.nombreComun} - {self.fecha.strftime('%d/%m/%Y')}"