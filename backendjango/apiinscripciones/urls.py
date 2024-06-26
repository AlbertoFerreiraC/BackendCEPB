from django.urls import path
from .views import generar_pdf, generar_pagare_pdf, genera_ficha_pdf, inscripciones_list, inscripcion_create, inscripcion_anular

urlpatterns = [
    path('', inscripciones_list, name='inscripciones_list'),
    path('create/', inscripcion_create, name='inscripcion_create'),
    path('anular/<int:id>/', inscripcion_anular, name='inscripcion_anular'),
    path('generar_pagare_pdf/<int:id>/', generar_pagare_pdf, name='generar_pagare_pdf'),
    path('genera_ficha_pdf/<int:id>/', genera_ficha_pdf, name='genera_ficha_pdf'),
    path('generar_pdf/<int:id>/', generar_pdf, name='generar_pdf'),
]
