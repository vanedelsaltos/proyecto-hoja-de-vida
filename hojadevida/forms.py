from django import forms
from .models import DatosPersonales
from .models import ExperienciaLaboral
from .models import CursosRealizados
from .models import Reconocimientos
from .models import ProductosAcademicos
from .models import ProductosLaborales
from .models import VentaGarage


#----------------FORMULARIO PARA LOS DATOS PERSONALES----------------
class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = [
            'perfilactivo',
            'descripcionperfil',
            'texto_inicio',
            'apellidos',
            'nombres',
            'foto_perfil',
            'nacionalidad',
            'lugarnacimiento',
            'fechanacimiento',
            'numerocedula',
            'sexo',
            'estadocivil',
            'licenciaconducir',
            'telefonoconvencional',
            'telefonofijo',
            'direcciontrabajo',
            'direcciondomiciliaria',
            'sitioweb',
            'es_activo',

        ]
        widgets = {
            'fechanacimiento': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'  # Formato que entiende <input type="date">
            ),
        }


#----------------FORMULARIO PARA EXPERIENCIA LABORAL----------------
class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = [
            'cargo_desempenado',
            'nombre_empresa',
            'lugar_empresa',
            'email_empresa',
            'sitio_web_empresa',
            'nombre_contacto_empresarial',
            'telefono_contacto_empresarial',
            'fecha_inicio_gestion',
            'fecha_fin_gestion',
            'descripcion_funciones',
            'certificado',
            'activar_para_front',
        ]
        widgets = {
            'fecha_inicio_gestion': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_fin_gestion': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


#----------------FORMULARIO PARA CURSOS REALIZADOS----------------
class CursosRealizadosForm(forms.ModelForm):
    class Meta:
        model = CursosRealizados
        fields = [
            'nombrecurso',
            'fechainicio',
            'fechafin',
            'totalhoras',
            'descripcioncurso',
            'entidadpatrocinadora',
            'nombrecontactoauspicia',
            'telefonocontactoauspicia',
            'emailempresapatrocinadora',
            'certificado',
            'activar_para_front',
        ]
        widgets = {
            'fechainicio': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fechafin': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


#----------------FORMULARIO PARA RECONOCIMIENTOS----------------
class ReconocimientosForm(forms.ModelForm):
    class Meta:
        model = Reconocimientos
        fields = [
            'tiporeconocimiento',
            'fechareconocimiento',
            'descripcionreconocimiento',
            'entidadpatrocinadora',
            'nombrecontactoauspicia',
            'telefonocontactoauspicia',
            'certificado',
            'activar_para_front',
        ]
        widgets = {
            'fechareconocimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


#----------------FORMULARIO PARA PRODUCTOS ACADÉMICOS----------------
class ProductosAcademicosForm(forms.ModelForm):
    class Meta:
        model = ProductosAcademicos
        fields = [
            'nombrerecurso',
            'clasificador',
            'descripcion',
            'imagen',
            'activar_para_front',
        ]


#----------------FORMULARIO PARA PRODUCTOS LABORALES----------------
class ProductosLaboralesForm(forms.ModelForm):
    class Meta:
        model = ProductosLaborales
        fields = [
            'nombreproducto',
            'tipoproducto',
            'fecha_producto',
            'descripcion',
            'activar_para_front',
        ]
        widgets = {
            'fecha_producto': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


#----------------FORMULARIO PARA VENTA DE GARAJE----------------
class VentaGarageForm(forms.ModelForm):
    class Meta:
        model = VentaGarage
        fields = [
            'nombreproducto',
            'estadoproducto',
            'descripcion',
            'valordelbien',
            'activar_para_front',
        ]
