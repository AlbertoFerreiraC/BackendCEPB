from django.contrib import admin
from .models import Alumno

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('alum_id', 'alum_ci', 'alum_nom', 'alum_ape', 'alum_fecha_nac', 'alum_edad')
    search_fields = ('alum_nom', 'alum_ape', 'alum_ci')
admin.site.register(Alumno, AlumnoAdmin)

