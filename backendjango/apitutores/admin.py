from django.contrib import admin
from .models import Tutor,TutorAlumno
class TutorAdmin(admin.ModelAdmin):
 list_display = ('tut_id', 'tut_ci', 'tut_nom', 'tut_ape', 'tut_tipo', 'tut_tel', 'tut_mail')
 search_fields = ('tut_nom', 'tut_ape', 'tut_ci', 'tut_mail')
class TutorAlumnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'tutor')
    search_fields = ('alumno__alum_nom', 'tutor__tut_nom')
admin.site.register(Tutor, TutorAdmin)
admin.site.register(TutorAlumno, TutorAlumnoAdmin)
# Register your models here.
