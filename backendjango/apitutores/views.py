from rest_framework import generics
from .models import Tutor, TutorAlumno
from .serializers import TutorSerializer, TutorAlumnoSerializer

class TutorListCreate(generics.ListCreateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

class TutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

class TutorAlumnoListCreate(generics.ListCreateAPIView):
    queryset = TutorAlumno.objects.all()
    serializer_class = TutorAlumnoSerializer

class TutorAlumnoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TutorAlumno.objects.all()
    serializer_class = TutorAlumnoSerializer
