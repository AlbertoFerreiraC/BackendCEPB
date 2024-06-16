from django.db import models
from apialumnos.models import Alumno

class Tutor(models.Model):
    TIPOS_CHOICES = (
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Tutor legal', 'Tutor legal'),
        ('Otro', 'Otro'),
    )
    tut_id = models.AutoField(primary_key=True)
    tut_ci = models.CharField(max_length=8)
    tut_tipo = models.CharField(max_length=20, choices=TIPOS_CHOICES)
    tut_nom = models.CharField(max_length=100)
    tut_ape = models.CharField(max_length=100)
    tut_tel = models.CharField(max_length=20)
    tut_direc = models.CharField(max_length=200)
    tut_mail = models.EmailField()

    def __str__(self):
        return f"{self.tut_nom} {self.tut_ape}"

    class Meta:
        ordering = ['tut_nom']

class TutorAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tutor {self.tutor} - Alumno {self.alumno}"

    class Meta:
        unique_together = ('alumno', 'tutor')  # Garantiza que no haya duplicados de alumno-tutor