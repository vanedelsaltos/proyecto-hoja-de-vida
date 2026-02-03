from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
import os

from .forms import (
    DatosPersonalesForm,
    ExperienciaLaboralForm,
    CursosRealizadosForm,
    ReconocimientosForm,
    ProductosAcademicosForm,
    ProductosLaboralesForm,
    VentaGarageForm
)

from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage
)

# -------------------------------------------------
# PERFIL ACTIVO
# -------------------------------------------------
def obtener_perfil_activo():
    perfil = DatosPersonales.objects.filter(es_activo=True).first()
    if perfil is None:
        perfil = DatosPersonales.objects.first()
    return perfil


# -------------------------------------------------
# HOME
# -------------------------------------------------
def home(request):
    return render(request, "home.html")


# -------------------------------------------------
# PANEL PRIVADO
# -------------------------------------------------
@login_required
def inicio(request):
    perfil = obtener_perfil_activo()
    if perfil is None:
        return redirect('crear_perfil')
    return render(request, 'inicio.html', {'perfil': perfil})


# -------------------------------------------------
# DATOS PERSONALES
# -------------------------------------------------
@login_required
def datos_personales(request):
    perfil = obtener_perfil_activo()
    if not perfil:
        return render(request, 'error.html', {'mensaje': 'No hay un perfil activo'})
    return render(request, 'perfil_y_datospersonales/datospersonales.html', {'perfil': perfil})




# LISTA DE PERFILES
@login_required
def lista_perfiles(request):
    perfiles = DatosPersonales.objects.all().order_by('-es_activo')
    return render(request, 'perfil_y_datospersonales/lista_perfiles.html', {'perfiles': perfiles})



# ACTIVAR PERFIL
@login_required
def activar_perfil(request, perfil_id):
    perfil = get_object_or_404(DatosPersonales, id=perfil_id)
    perfil.es_activo = True
    perfil.save()
    return redirect('lista_perfiles')


# CREAR PERFIL
@login_required
def crear_perfil(request):
    if request.method == 'POST':
        form = DatosPersonalesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_perfiles')
    else:
        form = DatosPersonalesForm()
    return render(request, 'perfil_y_datospersonales/form_datos_personales.html', {'form': form, 'accion': 'Crear'})


# EDITAR PERFIL
@login_required
def editar_perfil(request, perfil_id):
    perfil = get_object_or_404(DatosPersonales, id=perfil_id)
    if request.method == 'POST':
        form = DatosPersonalesForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('lista_perfiles')
    else:
        form = DatosPersonalesForm(instance=perfil)
    return render(request, 'perfil_y_datospersonales/form_datos_personales.html', {'form': form, 'accion': 'Guardar cambios'})


# ELIMINAR PERFIL
@login_required
def eliminar_perfil(request, perfil_id):
    perfil = get_object_or_404(DatosPersonales, id=perfil_id)
    if perfil.es_activo:
        return render(request, 'error.html', {'mensaje': 'No se puede eliminar el perfil activo.'})
    if request.method == 'POST':
        perfil.delete()
        return redirect('lista_perfiles')
    return render(request, 'confirmar_eliminar.html', {'perfil': perfil})


# -------------------------------------------------
# EXPERIENCIA LABORAL
# -------------------------------------------------
@login_required
def experiencia(request):
    perfil = obtener_perfil_activo()
    # Mostrar todas las experiencias del perfil, sin importar activar_para_front
    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil)
    # Si quieres que solo un usuario administrador vea todos los perfiles, puedes hacer algo como:
    # if request.user.is_superuser:
    #     experiencias = ExperienciaLaboral.objects.all()
    return render(request, 'experiencia/experiencia_lista.html', {'perfil': perfil, 'experiencias': experiencias})


@login_required
def crear_experiencia(request):
    perfil = obtener_perfil_activo()
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, request.FILES)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.idperfilconqueestaactivo = perfil
            experiencia.save()
            return redirect('experiencia')
    else:
        form = ExperienciaLaboralForm()
    return render(request, 'experiencia/experiencia_form.html', {'form': form, 'perfil': perfil})


@login_required
def editar_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=experiencia_id)
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, request.FILES, instance=experiencia)
        if form.is_valid():
            form.save()
            return redirect('experiencia')
    else:
        form = ExperienciaLaboralForm(instance=experiencia)
    return render(request, 'experiencia/experiencia_form.html', {'form': form})


@login_required
def eliminar_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=experiencia_id)
    experiencia.delete()
    return redirect('experiencia')


# -------------------------------------------------
# RECONOCIMIENTOS
# -------------------------------------------------
@login_required
def reconocimientos_lista(request):
    perfil = obtener_perfil_activo()
    reconocimientos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil)
    return render(request, 'reconocimientos/reconocimientos_lista.html', {'perfil': perfil, 'reconocimientos': reconocimientos})


@login_required
def crear_reconocimiento(request):
    perfil = obtener_perfil_activo()

    if not perfil:
        return redirect('crear_perfil')

    if request.method == 'POST':
        form = ReconocimientosForm(request.POST, request.FILES)
        if form.is_valid():
            reconocimiento = form.save(commit=False)
            reconocimiento.idperfilconqueestaactivo = perfil
            reconocimiento.save()
            return redirect('reconocimientos_lista')
    else:
        form = ReconocimientosForm()

    return render(
        request,
        'reconocimientos/reconocimientos_form.html',
        {'form': form, 'perfil': perfil}
    )



@login_required
def editar_reconocimiento(request, reconocimiento_id):
    reconocimiento = get_object_or_404(Reconocimientos, pk=reconocimiento_id)
    if request.method == 'POST':
        form = ReconocimientosForm(request.POST, request.FILES, instance=reconocimiento)
        if form.is_valid():
            form.save()
            return redirect('reconocimientos_lista')
    else:
        form = ReconocimientosForm(instance=reconocimiento)
    return render(request, 'reconocimientos/reconocimientos_form.html', {'form': form})


@login_required
def eliminar_reconocimiento(request, reconocimiento_id):
    reconocimiento = get_object_or_404(Reconocimientos, pk=reconocimiento_id)
    reconocimiento.delete()
    return redirect('reconocimientos_lista')


# -------------------------------------------------
# CURSOS REALIZADOS
# -------------------------------------------------
@login_required
def cursos_realizados(request):
    perfil = obtener_perfil_activo()
    cursos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil)
    return render(request, 'cursos/cursos_lista.html', {'perfil': perfil, 'cursos': cursos})


@login_required
def crear_curso(request):
    perfil = obtener_perfil_activo()
    if request.method == 'POST':
        form = CursosRealizadosForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.idperfilconqueestaactivo = perfil
            curso.save()
            return redirect('cursos_realizados')
    else:
        form = CursosRealizadosForm()
    return render(request, 'cursos/cursos_form.html', {'form': form, 'perfil': perfil})


@login_required
def editar_curso(request, curso_id):
    curso = get_object_or_404(CursosRealizados, pk=curso_id)
    if request.method == 'POST':
        form = CursosRealizadosForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('cursos_realizados')
    else:
        form = CursosRealizadosForm(instance=curso)
    return render(request, 'cursos/cursos_form.html', {'form': form})


@login_required
def eliminar_curso(request, curso_id):
    curso = get_object_or_404(CursosRealizados, pk=curso_id)
    curso.delete()
    return redirect('cursos_realizados')


# -------------------------------------------------
# PRODUCTOS ACADÉMICOS
# -------------------------------------------------
@login_required
def productos_academicos(request):
    perfil = obtener_perfil_activo()
    productos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil)
    return render(request, 'productos_academicos/productos_academicos.html', {'perfil': perfil, 'productos': productos})


@login_required
def crear_producto_academico(request):
    perfil = obtener_perfil_activo()
    if request.method == 'POST':
        form = ProductosAcademicosForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.idperfilconqueestaactivo = perfil
            producto.save()
            return redirect('productos_academicos')
    else:
        form = ProductosAcademicosForm()
    return render(request, 'productos_academicos/productos_academicos_form.html', {'form': form, 'perfil': perfil})


@login_required
def editar_producto_academico(request, producto_id):
    producto = get_object_or_404(ProductosAcademicos, pk=producto_id)
    if request.method == 'POST':
        form = ProductosAcademicosForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos_academicos')
    else:
        form = ProductosAcademicosForm(instance=producto)
    return render(request, 'productos_academicos/productos_academicos_form.html', {'form': form})


@login_required
def eliminar_producto_academico(request, producto_id):
    producto = get_object_or_404(ProductosAcademicos, pk=producto_id)
    producto.delete()
    return redirect('productos_academicos')


# -------------------------------------------------
# PRODUCTOS LABORALES
# -------------------------------------------------
@login_required
def productos_laborales(request):
    perfil = obtener_perfil_activo()
    productos = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil)
    return render(request, 'productos_laborales/productos_laborales.html', {'perfil': perfil, 'productos': productos})


@login_required
def crear_producto_laboral(request):
    perfil = obtener_perfil_activo()
    if request.method == 'POST':
        form = ProductosLaboralesForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.idperfilconqueestaactivo = perfil
            producto.save()
            return redirect('productos_laborales')
    else:
        form = ProductosLaboralesForm()
    return render(request, 'productos_laborales/productos_laborales_form.html', {'form': form, 'perfil': perfil})


@login_required
def editar_producto_laboral(request, producto_id):
    producto = get_object_or_404(ProductosLaborales, pk=producto_id)
    if request.method == 'POST':
        form = ProductosLaboralesForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos_laborales')
    else:
        form = ProductosLaboralesForm(instance=producto)
    return render(request, 'productos_laborales/productos_laborales_form.html', {'form': form})


@login_required
def eliminar_producto_laboral(request, producto_id):
    producto = get_object_or_404(ProductosLaborales, pk=producto_id)
    producto.delete()
    return redirect('productos_laborales')


# -------------------------------------------------
# VENTA DE GARAGE
# -------------------------------------------------
@login_required
def venta_garage(request):
    perfil = obtener_perfil_activo()
    ventas = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil)
    return render(request, 'venta_garage/venta_garage.html', {'perfil': perfil, 'ventas': ventas})


@login_required
def crear_venta_garage(request):
    perfil = obtener_perfil_activo()
    if request.method == 'POST':
        form = VentaGarageForm(request.POST, request.FILES)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.idperfilconqueestaactivo = perfil
            venta.save()
            return redirect('venta_garage')
    else:
        form = VentaGarageForm()
    return render(request, 'venta_garage/venta_garage_form.html', {'form': form, 'perfil': perfil})


@login_required
def editar_venta_garage(request, venta_id):
    venta = get_object_or_404(VentaGarage, pk=venta_id)
    if request.method == 'POST':
        form = VentaGarageForm(request.POST, request.FILES, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('venta_garage')
    else:
        form = VentaGarageForm(instance=venta)
    return render(request, 'venta_garage/venta_garage_form.html', {'form': form})


@login_required
def eliminar_venta_garage(request, venta_id):
    venta = get_object_or_404(VentaGarage, pk=venta_id)
    venta.delete()
    return redirect('venta_garage')


# -------------------------------------------------
# PÁGINA PÚBLICA (SIN LOGIN)
# -------------------------------------------------
def publico_inicio(request):
    perfil = obtener_perfil_activo()
    return render(request, 'publico/inicio.html', {'perfil': perfil})

def publico_datos(request):
    perfil = obtener_perfil_activo()
    return render(request, 'publico/datos.html', {'perfil': perfil})

def publico_experiencia(request):
    perfil = obtener_perfil_activo()
    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    return render(request, 'publico/experiencia.html', {'perfil': perfil, 'experiencias': experiencias})

def publico_cursos(request):
    perfil = obtener_perfil_activo()
    cursos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    return render(request, 'publico/cursos.html', {'perfil': perfil, 'cursos': cursos})

def publico_reconocimientos(request):
    perfil = obtener_perfil_activo()
    reconocimientos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    return render(request, 'publico/reconocimientos.html', {'perfil': perfil, 'reconocimientos': reconocimientos})

def publico_productos_academicos(request):
    perfil = obtener_perfil_activo()
    productos_academicos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    return render(request, 'publico/productos_academicos.html', {'perfil': perfil, 'productos_academicos': productos_academicos})

def publico_productos_laborales(request):
    perfil = obtener_perfil_activo()
    productos_laborales = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    return render(request, 'publico/productos_laborales.html', {'perfil': perfil, 'productos_laborales': productos_laborales})

def publico_venta_garage(request):
    perfil = obtener_perfil_activo()
    ventas = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    return render(request, 'publico/venta_garage.html', {'perfil': perfil, 'ventas': ventas})















# -------------------------------------------------
# IMPRIMIR HOJA DE VIDA (PDF)
# -------------------------------------------------
def imprimir_hoja_de_vida(request):
    """
    Genera el PDF con la información seleccionada
    por el usuario en el formulario de secciones.
    Si no se selecciona nada, se generan todas las secciones.
    """
    perfil = obtener_perfil_activo()
    if not perfil:
        return HttpResponse("No hay perfil activo para generar el PDF.")

    # -------------------------
    # Obtener qué secciones incluir desde GET
    # -------------------------
    # Si request.GET está vacío, incluimos TODO
    # Sin valor por defecto: si no está marcado, no se incluye
    incluir_experiencia = request.GET.get('experiencia') == 'on'
    incluir_cursos = request.GET.get('cursos') == 'on'
    incluir_reconocimientos = request.GET.get('reconocimientos') == 'on'
    incluir_productos_academicos = request.GET.get('productos_academicos') == 'on'
    incluir_productos_laborales = request.GET.get('productos_laborales') == 'on'
    incluir_ventas = request.GET.get('ventas') == 'on'


    # -------------------------
    # Filtrar los datos según selección
    # -------------------------
    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True) if incluir_experiencia else []
    cursos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True) if incluir_cursos else []
    reconocimientos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True) if incluir_reconocimientos else []
    productos_academicos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True) if incluir_productos_academicos else []
    productos_laborales = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True) if incluir_productos_laborales else []
    ventas = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True) if incluir_ventas else []

    # -------------------------
    # Filtrar solo certificados que tengan imagen
    # -------------------------
    certificados_experiencias = experiencias.filter(imagen_certificado__isnull=False).exclude(imagen_certificado='') if incluir_experiencia else []
    certificados_reconocimientos = reconocimientos.filter(imagen_certificado__isnull=False).exclude(imagen_certificado='') if incluir_reconocimientos else []
    certificados_cursos = cursos.filter(imagen_certificado__isnull=False).exclude(imagen_certificado='') if incluir_cursos else []

    # -------------------------
    # Renderizar HTML del PDF
    # -------------------------
    html_string = render_to_string("pdf/hoja_de_vida.html", {
        "perfil": perfil,
        "experiencias": experiencias,
        "cursos": cursos,
        "reconocimientos": reconocimientos,
        "productos_academicos": productos_academicos,  # se muestra solo texto
        "productos_laborales": productos_laborales,    # se muestra solo texto
        "ventas": ventas,
        # CERTIFICADOS
        "certificados_experiencias": certificados_experiencias,
        "certificados_reconocimientos": certificados_reconocimientos,
        "certificados_cursos": certificados_cursos,
        "STATIC_URL": request.build_absolute_uri(settings.STATIC_URL),
    })

    # -------------------------
    # Generar PDF
    # -------------------------
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="hoja_de_vida.pdf"'

    css_path = os.path.join(settings.STATIC_ROOT, 'css', 'hoja_de_vida.css')

    HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')
    ).write_pdf(
        response,
        stylesheets=[CSS(filename=css_path)]
    )

    return response


# -------------------------------------------------
# SELECCIONAR SECCIONES PARA PDF
# -------------------------------------------------
@login_required
def seleccionar_secciones_pdf(request):
    """
    Muestra un formulario con checkboxes para que el usuario
    seleccione qué secciones incluir en el PDF.
    Al enviar, redirige a imprimir_hoja_de_vida con los parámetros GET.
    """
    perfil = obtener_perfil_activo()
    if not perfil:
        return HttpResponse("No hay perfil activo para generar el PDF.")

    if request.method == 'GET' and 'generar_pdf' in request.GET:
        # Recoger las secciones marcadas
        params = {
            'experiencia': 'on' if request.GET.get('experiencia') == 'on' else '',
            'cursos': 'on' if request.GET.get('cursos') == 'on' else '',
            'reconocimientos': 'on' if request.GET.get('reconocimientos') == 'on' else '',
            'productos_academicos': 'on' if request.GET.get('productos_academicos') == 'on' else '',
            'productos_laborales': 'on' if request.GET.get('productos_laborales') == 'on' else '',
            'ventas': 'on' if request.GET.get('ventas') == 'on' else '',
        }
        # Construir la URL con parámetros GET
        query_string = "&".join([f"{k}={v}" for k, v in params.items() if v])
        return redirect(f"{reverse('imprimir_hoja_de_vida')}?{query_string}")

    # Mostrar formulario de selección
    return render(request, "pdf/seleccionar_secciones.html", {"perfil": perfil})
