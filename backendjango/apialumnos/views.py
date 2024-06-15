from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Alumno
from .serializers import AlumnoSerializer

@api_view(['GET', 'POST'])
def alumnos_list(request):
    if request.method == 'GET':
        alumnos = Alumno.objects.all()
        serializer = AlumnoSerializer(alumnos, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        serializer = AlumnoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)  # 201 Created
        return JsonResponse(serializer.errors, status=400)  # Bad request

@api_view(['GET'])
def alumno_detail(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    serializer = AlumnoSerializer(alumno)
    return JsonResponse(serializer.data, safe=False)
