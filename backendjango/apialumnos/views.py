from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Alumno
from .serializers import AlumnoSerializer
from rest_framework.decorators import api_view
@api_view(['GET'])
def alumnos_list(request):
    alumnos = Alumno.objects.all()
    serializer = AlumnoSerializer(alumnos, many=True)
    return JsonResponse(serializer.data, safe=False)
@api_view(['GET'])
def alumno_detail(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    serializer = AlumnoSerializer(alumno)
    return JsonResponse(serializer.data, safe=False)
# Create your views here