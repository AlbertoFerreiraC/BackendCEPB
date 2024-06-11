from django.contrib import admin
from .models import Inscripcion,Arancel
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tutor_alumno', 'ins_fecha', 'ins_descuento', 'ins_contrato_fecha')
    search_fields = ('tutor_alumno__tutor__tut_nom', 'tutor_alumno__alumno__alum_nom')
    ist_filter = ('ins_fecha', 'ins_descuento')
admin.site.register(Inscripcion, InscripcionAdmin)
class ArancelAdmin(admin.ModelAdmin):
    list_display = ['inscripcion', 'arancel_nivel', 'arancel_cuota']
admin.site.register(Arancel, ArancelAdmin)
# Register your models here.
