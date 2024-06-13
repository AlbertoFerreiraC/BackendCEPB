from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html  # Asegúrate de importar format_html
from .models import Inscripcion, Arancel

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tutor_alumno', 'ins_fecha', 'ins_descuento', 'ins_contrato_fecha', 'generar_pagare_pdf_link')
    search_fields = ('tutor_alumno__tutor__tut_nom', 'tutor_alumno__alumno__alum_nom')
    list_filter = ('ins_fecha', 'ins_descuento')
    actions = ['generar_pdf_action', 'generar_pagare_pdf_action']

    def generar_pdf_action(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Por favor seleccione exactamente una inscripción.")
            return

        inscripcion_id = queryset.first().id
        return HttpResponseRedirect(reverse('generar_pdf', kwargs={'id': inscripcion_id}))
    generar_pdf_action.short_description = "Generar PDF de contrato"

    def generar_pagare_pdf_action(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Por favor seleccione exactamente una inscripción.")
            return

        inscripcion_id = queryset.first().id
        return HttpResponseRedirect(reverse('generar_pagare_pdf', kwargs={'id': inscripcion_id}))
    generar_pagare_pdf_action.short_description = "Generar PDF del pagaré"

    def generar_pagare_pdf_link(self, obj):
        url = reverse('generar_pagare_pdf', args=[obj.id])
        return format_html('<a href="{}" target="_blank">Generar pagaré PDF</a>', url)
    generar_pagare_pdf_link.short_description = 'Generar pagaré PDF'

admin.site.register(Inscripcion, InscripcionAdmin)

class ArancelAdmin(admin.ModelAdmin):
    list_display = ['inscripcion', 'arancel_nivel', 'arancel_cuota']

admin.site.register(Arancel, ArancelAdmin)
