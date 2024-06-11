from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Tutor, TutorAlumno
from .serializers import TutorSerializer, TutorAlumnoSerializer
from rest_framework.decorators import api_view

@api_view(['GET'])
def tutor_list(request):
    tutores = Tutor.objects.all()
    serializer = TutorSerializer(tutores, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def tutor_detail(request, id):
    tutor = get_object_or_404(Tutor, id=id)
    serializer = TutorSerializer(tutor)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def tutor_alumno_list(request):
    tutor_alumnos = TutorAlumno.objects.all()
    serializer = TutorAlumnoSerializer(tutor_alumnos, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def tutor_alumno_detail(request, id):
    tutor_alumno = get_object_or_404(TutorAlumno, id=id)
    serializer = TutorAlumnoSerializer(tutor_alumno)
    return JsonResponse(serializer.data, safe=False)
