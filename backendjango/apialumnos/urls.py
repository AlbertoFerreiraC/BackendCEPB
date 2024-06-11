from django.urls import path
from .views import alumnos_list, alumno_detail

urlpatterns = [
    path('', alumnos_list, name='alumnos_list'),
    path('<int:id>/', alumno_detail, name='alumno_detail'),
]

