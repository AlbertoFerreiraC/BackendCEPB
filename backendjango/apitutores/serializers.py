from rest_framework import serializers
from .models import Tutor, TutorAlumno
from apialumnos.serializers import AlumnoSerializer  # Asegúrate de importar tu serializer de Alumno

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'

class TutorAlumnoSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer()  # Serializer anidado para incluir detalles completos de Tutor
    alumno = AlumnoSerializer()  # Serializer anidado para incluir detalles completos de Alumno

    class Meta:
        model = TutorAlumno
        fields = ['id', 'alumno', 'tutor']  # Incluye todos los campos necesarios aquí según tus requerimientos
