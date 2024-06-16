from rest_framework import generics
from .models import Tutor, TutorAlumno
from .serializers import TutorSerializer, TutorAlumnoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class TutorListCreate(generics.ListCreateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Utiliza prefetch_related para cargar la relación a través de TutorAlumno
        return queryset.prefetch_related('tutoralumno_set__alumno')

class TutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

class TutorAlumnoListCreate(generics.ListCreateAPIView):
    queryset = TutorAlumno.objects.all()
    serializer_class = TutorAlumnoSerializer

class TutorAlumnoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TutorAlumno.objects.all()
    serializer_class = TutorAlumnoSerializer

class TutorAlumnoCreate(APIView):
    def post(self, request, format=None):
        serializer = TutorAlumnoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)