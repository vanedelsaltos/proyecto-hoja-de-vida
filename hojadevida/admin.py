from django.contrib import admin
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage
)


@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'perfilactivo', 'es_activo')
    list_filter = ('perfilactivo', 'es_activo')
    search_fields = ('nombres', 'apellidos', 'numerocedula')


@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = (
        'cargo_desempenado',
        'nombre_empresa',
        'idperfilconqueestaactivo',
        'activar_para_front'
    )
    list_filter = ('activar_para_front', 'idperfilconqueestaactivo')
    search_fields = ('cargo_desempenado', 'nombre_empresa')


@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = (
        'tiporeconocimiento',
        'fechareconocimiento',
        'idperfilconqueestaactivo',
        'activar_para_front'
    )
    list_filter = ('tiporeconocimiento', 'activar_para_front')
    search_fields = ('descripcionreconocimiento', 'entidadpatrocinadora')


@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = (
        'nombrecurso',
        'fechainicio',
        'fechafin',
        'idperfilconqueestaactivo',
        'activar_para_front'
    )
    list_filter = ('activar_para_front',)
    search_fields = ('nombrecurso', 'entidadpatrocinadora')


@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activar_para_front')
    list_filter = ('activar_para_front',)


@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'tipoproducto', 'fecha_producto', 'activar_para_front')
    list_filter = ('activar_para_front',)


@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'estadoproducto', 'valordelbien', 'activar_para_front')
    list_filter = ('estadoproducto', 'activar_para_front')
