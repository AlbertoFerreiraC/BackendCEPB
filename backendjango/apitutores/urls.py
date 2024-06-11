from django.urls import path
from .views import tutor_list, tutor_detail, tutor_alumno_list, tutor_alumno_detail

urlpatterns = [
    path('', tutor_list, name='tutor_list'),
    path('<int:id>/', tutor_detail, name='tutor_detail'),
    path('alumnos/', tutor_alumno_list, name='tutor_alumno_list'),
    path('alumnos/<int:id>/', tutor_alumno_detail, name='tutor_alumno_detail'),
]
