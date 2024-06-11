from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from .models import Inscripcion
from apialumnos.models import Alumno
from apitutores.models import Tutor, TutorAlumno
import json

def inscripciones_list(request):
    inscripciones = Inscripcion.objects.all()
    data = [{
        "id": inscripcion.id,
        "alumno": inscripcion.tutor_alumno.alumno.alum_nom,
        "tutor": inscripcion.tutor_alumno.tutor.tut_nom,
        "fecha_inscripcion": inscripcion.ins_fecha,
        "descuento": inscripcion.ins_descuento,
        "cuota": inscripcion.ins_cuota,
        "estado": inscripcion.ins_estado,
        "periodo": inscripcion.ins_periodo
    } for inscripcion in inscripciones]
    return JsonResponse({"inscripciones": data})

@csrf_exempt
def inscripcion_create(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            alumno_id = data.get("alumno_id")
            tutor_id = data.get("tutor_id")
            contrato_fecha = parse_date(data.get("contrato_fecha"))

            alumno = Alumno.objects.get(id=alumno_id)
            tutor = Tutor.objects.get(id=tutor_id)

            tutor_alumno, created = TutorAlumno.objects.get_or_create(alumno=alumno, tutor=tutor)
            
            inscripcion = Inscripcion.objects.create(
                tutor_alumno=tutor_alumno,
                ins_contrato_fecha=contrato_fecha
            )
            return JsonResponse({"message": "Inscripción creada exitosamente", "inscripcion_id": inscripcion.id})
        except (Alumno.DoesNotExist, Tutor.DoesNotExist):
            return JsonResponse({"error": "Alumno o Tutor no encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponseBadRequest("Método no permitido")

@csrf_exempt
def inscripcion_anular(request, id):
    if request.method == "DELETE":
        try:
            inscripcion = Inscripcion.objects.get(id=id)
            inscripcion.delete()
            return JsonResponse({"message": "Inscripción anulada exitosamente"})
        except Inscripcion.DoesNotExist:
            return JsonResponse({"error": "Inscripción no encontrada"}, status=404)
    return HttpResponseBadRequest("Método no permitido")
