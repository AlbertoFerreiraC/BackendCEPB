from django.db import models
from datetime import date
class Alumno(models.Model):
    alum_id = models.AutoField(primary_key=True)
    alum_ci = models.CharField(max_length=8)
    alum_nom = models.CharField(max_length=100)
    alum_ape = models.CharField(max_length=100)
    alum_fecha_nac = models.DateField()
    alum_edad = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):
        self.alum_edad = self.calcular_edad()
        super().save(*args, **kwargs)

    def calcular_edad(self):
        today = date.today()
        return today.year - self.alum_fecha_nac.year - ((today.month, today.day) < (self.alum_fecha_nac.month, self.alum_fecha_nac.day))

    def __str__(self):
        return f"{self.alum_nom} {self.alum_ape}"

# Create your models here.
