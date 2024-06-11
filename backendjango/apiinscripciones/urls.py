from django.urls import path
from .views import inscripciones_list, inscripcion_create, inscripcion_anular

urlpatterns = [
    path('', inscripciones_list, name='inscripciones_list'),
    path('create/', inscripcion_create, name='inscripcion_create'),
    path('anular/<int:id>/', inscripcion_anular, name='inscripcion_anular'),
]