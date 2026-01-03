from django.contrib import admin

# Register your models here.
from .models import DatosPersonales
from .models import ExperienciaLaboral
from .models import Reconocimientos
from .models import CursosRealizados
from .models import ProductosAcademicos
from .models import ProductosLaborales
from .models import VentaGarage

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'perfilactivo', 'es_activo')

    
admin.site.register(ExperienciaLaboral)
admin.site.register(Reconocimientos)
admin.site.register(CursosRealizados)
admin.site.register(ProductosAcademicos)
admin.site.register(ProductosLaborales)
admin.site.register(VentaGarage)



