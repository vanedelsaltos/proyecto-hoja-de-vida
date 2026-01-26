from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
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
    return render(request, 'datospersonales.html', {'perfil': perfil})


# LISTA DE PERFILES
@login_required
def lista_perfiles(request):
    perfiles = DatosPersonales.objects.all().order_by('-es_activo')
    return render(request, 'lista_perfiles.html', {'perfiles': perfiles})


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
    return render(request, 'form_datos_personales.html', {'form': form, 'accion': 'Crear'})


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
    return render(request, 'form_datos_personales.html', {'form': form, 'accion': 'Guardar cambios'})


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
    if request.method == 'POST':
        form = ReconocimientosForm(request.POST, request.FILES)
        if form.is_valid():
            reconocimiento = form.save(commit=False)
            reconocimiento.idperfilconqueestaactivo = perfil
            reconocimiento.save()
            return redirect('reconocimientos_lista')
    else:
        form = ReconocimientosForm()
    return render(request, 'reconocimientos/reconocimientos_form.html', {'form': form, 'perfil': perfil})


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
def publico(request):
    perfil = obtener_perfil_activo()
    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    cursos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    reconocimientos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    productos_academicos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    productos_laborales = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    ventas = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)

    return render(request, 'publico.html', {
        'perfil': perfil,
        'experiencias': experiencias,
        'cursos': cursos,
        'reconocimientos': reconocimientos,
        'productos_academicos': productos_academicos,
        'productos_laborales': productos_laborales,
        'ventas': ventas,
    })















# -------------------------------------------------
# IMPRIMIR HOJA DE VIDA (PDF)
# -------------------------------------------------
def imprimir_hoja_de_vida(request):
    """
    Genera el PDF con TODA la información
    que aparece en la página pública, dejando
    los certificados al final.
    """
    perfil = obtener_perfil_activo()
    if not perfil:
        return HttpResponse("No hay perfil activo para generar el PDF.")

    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    cursos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    reconocimientos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    productos_academicos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    productos_laborales = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True)
    # ventas = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activar_para_front=True) # No las queremos

    # -------------------------
    # Filtrar solo certificados que tengan imagen
    # -------------------------
    certificados_experiencias = experiencias.filter(imagen_certificado__isnull=False).exclude(imagen_certificado='')
    certificados_reconocimientos = reconocimientos.filter(imagen_certificado__isnull=False).exclude(imagen_certificado='')
    certificados_cursos = cursos.filter(imagen_certificado__isnull=False).exclude(imagen_certificado='')

    html_string = render_to_string("pdf/hoja_de_vida.html", {
        "perfil": perfil,
        "experiencias": experiencias,
        "cursos": cursos,
        "reconocimientos": reconocimientos,
        "productos_academicos": productos_academicos,  # se muestra solo texto
        "productos_laborales": productos_laborales,    # se muestra solo texto
        # CERTIFICADOS
        "certificados_experiencias": certificados_experiencias,
        "certificados_reconocimientos": certificados_reconocimientos,
        "certificados_cursos": certificados_cursos,
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="hoja_de_vida.pdf"'

    HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')
    ).write_pdf(response)

    return response

    

