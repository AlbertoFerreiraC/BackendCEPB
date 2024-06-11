from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Inscripcion, Arancel

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tutor_alumno', 'ins_fecha', 'ins_descuento', 'ins_contrato_fecha')
    search_fields = ('tutor_alumno__tutor__tut_nom', 'tutor_alumno__alumno__alum_nom')
    list_filter = ('ins_fecha', 'ins_descuento')

    def generar_pdf_action(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Por favor seleccione exactamente una inscripción.")
            return

        inscripcion_id = queryset.first().id

        # Redirigir a la vista para generar el PDF con el ID de la inscripción
        return HttpResponseRedirect(reverse('generar_pdf', kwargs={'id': inscripcion_id}))


    generar_pdf_action.short_description = "Generar PDF de contrato"
    actions = ['generar_pdf_action']

admin.site.register(Inscripcion, InscripcionAdmin)

class ArancelAdmin(admin.ModelAdmin):
    list_display = ['inscripcion', 'arancel_nivel', 'arancel_cuota']

admin.site.register(Arancel, ArancelAdmin)
