from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from .models import Inscripcion, Arancel
from apialumnos.models import Alumno
from apitutores.models import Tutor, TutorAlumno
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def inscripciones_list(request):
    inscripciones = Inscripcion.objects.all()
    data = []
    for inscripcion in inscripciones:
        tutor_alumno = inscripcion.tutor_alumno
        alumno_nombre = tutor_alumno.alumno.alum_nom
        tutor_nombre = tutor_alumno.tutor.tut_nom
        data.append({
            "id": inscripcion.id,
            "alumno": alumno_nombre,
            "tutor": tutor_nombre,
            "fecha_inscripcion": inscripcion.ins_fecha,
            "descuento": inscripcion.ins_descuento,
            "cuota": inscripcion.ins_cuota,
            "estado": inscripcion.ins_estado,
            "periodo": inscripcion.ins_periodo
        })
    return JsonResponse({"inscripciones": data})

@csrf_exempt
def inscripcion_create(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tutor_id = data.get("tutor")
            alumno_id = data.get("alumno")
            contrato_fecha = parse_date(data.get("ins_contrato_fecha"))
            periodo = data.get("ins_periodo")

            # Validar presencia de datos requeridos
            if not tutor_id or not alumno_id or not contrato_fecha or not periodo:
                return JsonResponse({"error": "Datos incompletos"}, status=400)

            # Recuperar tutor y alumno
            tutor = Tutor.objects.get(pk=tutor_id)
            alumno = Alumno.objects.get(pk=alumno_id)

            # Crear o recuperar relación Tutor-Alumno
            tutor_alumno, _ = TutorAlumno.objects.get_or_create(
                alumno=alumno,
                tutor=tutor
            )

            # Crear inscripción
            inscripcion = Inscripcion.objects.create(
                tutor_alumno=tutor_alumno,
                ins_contrato_fecha=contrato_fecha,
                ins_periodo=periodo,
                ins_estado='Inscripto'  # Por defecto, estado inicial
            )

            return JsonResponse({"message": "Inscripción creada exitosamente", "inscripcion_id": inscripcion.id})
        except KeyError as e:
            return JsonResponse({"error": f"Campo requerido faltante: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return HttpResponseNotAllowed(["POST"])  # Devuelve 405 solo si el método no es POST


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

def generar_pdf(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    tutor = inscripcion.tutor_alumno.tutor
    alumno = inscripcion.tutor_alumno.alumno
    arancel = inscripcion.aranceles.first()

    tutor_nombre = tutor.tut_nom
    tutor_apellido = tutor.tut_ape
    tutor_direccion = tutor.tut_direc
    alumno_nombre = alumno.alum_nom
    alumno_apellido = alumno.alum_ape
    arancel_matricula = arancel.arancel_matricula
    arancel_cuota = arancel.arancel_cuota
    arancel_nivel = arancel.arancel_nivel
    arancel_grado = arancel.arancel_grado

    contract_content = [
        ("CONTRATO DE SERVICIOS EDUCATIVOS", "CENTER", True),
        ("CENTRO EDUCATIVO PARAGUAY - BRASIL (CEPB)", "CENTER", True),
        (f'{tutor_nombre} {tutor_apellido} (en adelante "el/la Padre/Madre/Tutor") con domicilio en {tutor_direccion} actuando en nombre y representación del estudiante {alumno_nombre} {alumno_apellido}', "LEFT", True),
        ("Se acuerda lo siguiente:", "LEFT", True),
        ("Primero: Objeto", "LEFT", True),
        ("CEPB se compromete a brindar servicios educativos de acuerdo a los programas oficiales y normas establecidas por el Ministerio de Educación, y el/la Padre/Madre/Tutor se compromete a cumplir con las condiciones aquí establecidas.", "JUSTIFY", False),
        ("Segundo: Duración", "LEFT", True),
        ("El presente contrato tendrá una duración de un (1) año lectivo.", "JUSTIFY", False),
        ("Tercero: DERECHOS Y OBLIGACIONES DE CEPB", "LEFT", True),
        ("Proveer educación integral conforme al currículo vigente. Facilitar el acceso a instalaciones adecuadas y seguras. Ofrecer actividades extracurriculares y servicios adicionales, según lo estipulado. Evaluar y reportar el desempeño académico y comportamental del estudiante periódicamente. Garantizar un entorno educativo libre de discriminación y acoso.", "JUSTIFY", False),
        ("CUARTO: DERECHOS Y OBLIGACIONES DEL/LA PADRE/MADRE/TUTOR", "LEFT", True),
        ("Pagar puntualmente las matrículas y cuotas establecidas por CEPB. Asegurar que el estudiante cumpla con las normas y reglamentos del colegio. Participar en reuniones y actividades escolares convocadas por CEPB. Informar oportunamente sobre cualquier cambio en los datos del estudiante o familiares. Colaborar con el colegio en el seguimiento del progreso académico y conductual del estudiante.", "JUSTIFY", False),
        ("QUINTO: PAGO DE MATRÍCULAS Y CUOTAS", "LEFT", True),
        (f'El/la Padre/Madre/Tutor se compromete a pagar una matrícula anual de {arancel_matricula} y una cuota mensual de {arancel_cuota}, en el nivel {arancel_nivel}, y grado {arancel_grado}, en el que se encuentra el estudiante. Los pagos deben realizarse dentro de los primeros cinco días hábiles de cada mes. En caso de mora, se aplicará un recargo del 15% mensual sobre el monto adeudado.', "JUSTIFY", False),
        ("SEXTO: TERMINACIÓN DEL CONTRATO", "LEFT", True),
        ("El presente contrato podrá ser terminado por: Decisión unilateral del/la Padre/Madre/Tutor, con un aviso previo de treinta (30) días. Incumplimiento de las obligaciones aquí pactadas por cualquiera de las partes. Decisión del CEPB por razones disciplinarias graves o impago reiterado.", "JUSTIFY", False),
        ("SÉPTIMO: DISPOSICIONES GENERALES", "LEFT", True),
        ("Cualquier modificación a este contrato deberá hacerse por escrito y ser firmada por ambas partes.", "JUSTIFY", False)
    ]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contrato_servicios_educativos.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    style_center = ParagraphStyle(name="Center", alignment=TA_CENTER)
    style_left = ParagraphStyle(name="Left", alignment=TA_LEFT)
    style_justify = ParagraphStyle(name="Justify", alignment=TA_JUSTIFY)

    for text, alignment, is_bold in contract_content:
        style = style_center if alignment == "CENTER" else (style_left if alignment == "LEFT" else style_justify)
        if is_bold:
            style.fontName = "Helvetica-Bold"
        elements.append(Paragraph(text, style))

    doc.build(elements)
    return response

def generar_pagare_pdf(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    tutor = inscripcion.tutor_alumno.tutor
    alumno = inscripcion.tutor_alumno.alumno
    arancel = inscripcion.aranceles.first()

    tutor_nombre = tutor.tut_nom
    tutor_apellido = tutor.tut_ape
    tutor_direccion = tutor.tut_direc
    tutor_ci = tutor.tut_ci
    alumno_nombre = alumno.alum_nom
    alumno_apellido = alumno.alum_ape
    arancel_matricula = arancel.arancel_matricula
    arancel_cuota = arancel.arancel_cuota
    arancel_nivel = arancel.arancel_nivel
    arancel_grado = arancel.arancel_grado

    pagare_content = [
        ("PAGARÉ", "CENTER", True),
        (f"Yo, {tutor_nombre} {tutor_apellido}, con C.I. {tutor_ci} y domiciliado en {tutor_direccion}, me obligo a pagar a la orden del CENTRO EDUCATIVO PARAGUAY - BRASIL (CEPB) la suma de {arancel_matricula + arancel_cuota} guaraníes.", "JUSTIFY", False),
        (f"Este pagaré corresponde al pago de la matrícula y la cuota del estudiante {alumno_nombre} {alumno_apellido}.", "JUSTIFY", False),
        (f"La suma mencionada será pagada en cuotas mensuales de {arancel_cuota} guaraníes cada una, con vencimiento el primer día de cada mes.", "JUSTIFY", False),
        ("En caso de mora en el pago de cualquier cuota, se aplicará un recargo del 15% mensual sobre el monto adeudado.", "JUSTIFY", False),
        ("Lugar y Fecha", "LEFT", True),
        ("____________________________", "LEFT", True),
        ("Firma del Deudor", "LEFT", True),
    ]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pagare_{inscripcion.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    style_center = ParagraphStyle(name="Center", alignment=TA_CENTER)
    style_left = ParagraphStyle(name="Left", alignment=TA_LEFT)
    style_justify = ParagraphStyle(name="Justify", alignment=TA_JUSTIFY)

    for text, alignment, is_bold in pagare_content:
        style = style_center if alignment == "CENTER" else (style_left if alignment == "LEFT" else style_justify)
        if is_bold:
            style.fontName = "Helvetica-Bold"
        elements.append(Paragraph(text, style))

    doc.build(elements)
    return response

def genera_ficha_pdf(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    tutor = inscripcion.tutor_alumno.tutor
    alumno = inscripcion.tutor_alumno.alumno
    arancel = inscripcion.aranceles.first()

    tutor_nombre = tutor.tut_nom
    tutor_apellido = tutor.tut_ape
    tutor_direccion = tutor.tut_direc
    tutor_ci = tutor.tut_ci
    alumno_nombre = alumno.alum_nom
    alumno_apellido = alumno.alum_ape
    arancel_matricula = arancel.arancel_matricula
    arancel_cuota = arancel.arancel_cuota
    arancel_nivel = arancel.arancel_nivel
    arancel_grado = arancel.arancel_grado

    ficha_content = [
        ("FICHA DE INSCRIPCIÓN", "CENTER", True),
        (f"Tutor: {tutor_nombre} {tutor_apellido}", "LEFT", False),
        (f"C.I.: {tutor_ci}", "LEFT", False),
        (f"Dirección: {tutor_direccion}", "LEFT", False),
        (f"Alumno: {alumno_nombre} {alumno_apellido}", "LEFT", False),
        (f"Nivel: {arancel_nivel}", "LEFT", False),
        (f"Grado: {arancel_grado}", "LEFT", False),
        (f"Matrícula: {arancel_matricula} guaraníes", "LEFT", False),
        (f"Cuota: {arancel_cuota} guaraníes", "LEFT", False),
        ("Lugar y Fecha", "LEFT", True),
        ("____________________________", "LEFT", True),
        ("Firma del Tutor", "LEFT", True),
    ]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ficha_{alumno_nombre}_{alumno_apellido}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    style_center = ParagraphStyle(name="Center", alignment=TA_CENTER)
    style_left = ParagraphStyle(name="Left", alignment=TA_LEFT)
    style_justify = ParagraphStyle(name="Justify", alignment=TA_JUSTIFY)

    for text, alignment, is_bold in ficha_content:
        style = style_center if alignment == "CENTER" else (style_left if alignment == "LEFT" else style_justify)
        if is_bold:
            style.fontName = "Helvetica-Bold"
        elements.append(Paragraph(text, style))

    doc.build(elements)
    return response
