from django.urls import path
from .views import TutorListCreate, TutorDetail, TutorAlumnoListCreate, TutorAlumnoDetail

urlpatterns = [
    path('', TutorListCreate.as_view(), name='tutor_list'),
    path('<int:pk>/', TutorDetail.as_view(), name='tutor_detail'),
    path('alumnos/', TutorAlumnoListCreate.as_view(), name='tutor_alumno_list'),
    path('alumnos/<int:pk>/', TutorAlumnoDetail.as_view(), name='tutor_alumno_detail'),
]
