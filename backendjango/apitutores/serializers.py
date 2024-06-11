from rest_framework import serializers
from .models import Tutor,TutorAlumno
 
class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'
class TutorAlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorAlumno
        fields = '__all__'