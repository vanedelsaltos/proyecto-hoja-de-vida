from django.db import models
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField

from django.core.exceptions import ValidationError
from datetime import date

from django.utils import timezone


# ------------------------------------------------------------------------------------------------------------------------------------
#TABLA DE DATOS PERSONALES 

class DatosPersonales(models.Model):

    PERFIL_CHOICES = [
        (1, 'Perfil profesional'),
        (2, 'Perfil alternativo'),
        (3, 'Perfil personal'),
    ]

    SEXO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    ]

    perfilactivo = models.IntegerField(
        choices=PERFIL_CHOICES,
        verbose_name="Tipo perfil"
    )

    #ESTO ES LO NUEVO
    es_activo = models.BooleanField(
        default=False,
        verbose_name="Perfil activo"
    )


    descripcionperfil = models.CharField(
        max_length=100,
        verbose_name="Descripción del perfil"
    )

    apellidos = models.CharField(
        max_length=60,
        verbose_name="Apellidos"
    )

    nombres = models.CharField(
        max_length=60,
        verbose_name="Nombres"
    )

    #PARTE PARA AGREGAR UNA FOTO DE PERFIL
    foto_perfil = CloudinaryField(
        'foto_perfil',
        folder='perfil',
        blank=True,
        null=True
    )

    nacionalidad = models.CharField(
        max_length=50,
        verbose_name="Nacionalidad"
    )

    lugarnacimiento = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Lugar de nacimiento"
    )

    fechanacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de nacimiento"
    )

    numerocedula = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Número de cédula"
    )

    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        verbose_name="Sexo"
    )

    estadocivil = models.CharField(
        max_length=50,
        verbose_name="Estado civil"
    )

    licenciaconducir = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        verbose_name="Licencia de conducir"
    )

    telefonoconvencional = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Teléfono convencional"
    )

    telefonofijo = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Teléfono fijo"
    )

    direcciontrabajo = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Dirección de trabajo"
    )

    direcciondomiciliaria = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Dirección domiciliaria"
    )

    sitioweb = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name="Sitio web"
    )

    class Meta:
        verbose_name = "Datos personales"
        verbose_name_plural = "Datos personales"


    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def __str__(self):
        return f"{self.nombre_completo()} ({self.get_perfilactivo_display()})"

    # -----------------------------------------------------------------
    # Validaciones personalizadas
    def clean(self):
        # Validar fecha de nacimiento
        if self.fechanacimiento:
            if self.fechanacimiento > date.today():
                raise ValidationError({'fechanacimiento': "La fecha de nacimiento no puede ser futura"})

        # Validar cédula: solo números y 10 dígitos
        if self.numerocedula:
            if not self.numerocedula.isdigit():
                raise ValidationError({'numerocedula': "La cédula debe contener solo números"})
            if len(self.numerocedula) != 10:
                raise ValidationError({'numerocedula': "La cédula debe tener 10 dígitos"})

        # Validar teléfonos: solo números si se ingresan
        # Validar teléfonos
        # Teléfono convencional: solo números
        if self.telefonoconvencional:
            if not self.telefonoconvencional.isdigit():
                raise ValidationError({
                    'telefonoconvencional': "El teléfono convencional debe contener solo números"
                })

        # Teléfono fijo: solo números y exactamente 10 dígitos
        if self.telefonofijo:
            if not self.telefonofijo.isdigit():
                raise ValidationError({
                    'telefonofijo': "El teléfono fijo debe contener solo números"
                })
            if len(self.telefonofijo) != 10:
                raise ValidationError({
                    'telefonofijo': "El teléfono fijo debe tener exactamente 10 dígitos"
                })



    #ESTO LO QUE HACE ES FORZAR UN SOLO PERFIL ACTIVO
    def save(self, *args, **kwargs):
        self.full_clean()  # Esto asegura que se apliquen las validaciones antes de guardar
        if self.es_activo:
            DatosPersonales.objects.exclude(pk=self.pk).update(es_activo=False)
        super().save(*args, **kwargs)
        
    
# ------------------------------------------------------------------------------------------------------------------------------------

# tabla de experiencia laboral
class ExperienciaLaboral(models.Model):

    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='experiencias',
        verbose_name="Perfil al que pertenece"
    )

    # ================= DATOS PRINCIPALES =================
    cargo_desempenado = models.CharField(
        max_length=100,
        verbose_name="Cargo desempeñado"
    )

    nombre_empresa = models.CharField(
        max_length=50,
        verbose_name="Nombre de la empresa"
    )

    lugar_empresa = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Lugar de la empresa"
    )

    email_empresa = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email de la empresa"
    )

    sitio_web_empresa = models.URLField(
        blank=True,
        null=True,
        verbose_name="Sitio web de la empresa"
    )

    nombre_contacto_empresarial = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nombre del contacto empresarial"
    )

    telefono_contacto_empresarial = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name="Teléfono del contacto"
    )

    # ================= FECHAS =================
    fecha_inicio_gestion = models.DateField(
        verbose_name="Fecha de inicio"
    )

    fecha_fin_gestion = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de finalización"
    )

    # ================= DESCRIPCIÓN =================
    descripcion_funciones = models.TextField(
        blank=True,
        verbose_name="Descripción de funciones"
    )

    # ================= CERTIFICADO =================
    certificado = CloudinaryField(
        'certificado',
        resource_type='raw',
        folder='certificados/experiencia',
        blank=True,
        null=True
    )

    imagen_certificado = CloudinaryField(
        'Imagen del certificado',
        resource_type='image',
        folder='certificados/experiencia',
        blank=True,
        null=True
    )

    # ================= VISIBILIDAD =================
    activar_para_front = models.BooleanField(
        default=True,
        verbose_name="Mostrar en la página web"
    )

    class Meta:
        verbose_name = "Experiencia laboral"
        verbose_name_plural = "Experiencias laborales"
        ordering = ['-fecha_inicio_gestion']

    def __str__(self):
        return f"{self.cargo_desempenado} - {self.nombre_empresa}"

    # ================= VALIDACIONES =================
    def clean(self):
        today = date.today()

        # Fecha inicio no futura
        if self.fecha_inicio_gestion and self.fecha_inicio_gestion > today:
            raise ValidationError({
                'fecha_inicio_gestion': "La fecha de inicio no puede ser futura"
            })

        # Fecha fin no futura
        if self.fecha_fin_gestion and self.fecha_fin_gestion > today:
            raise ValidationError({
                'fecha_fin_gestion': "La fecha de finalización no puede ser futura"
            })

        # Fecha fin >= fecha inicio
        if self.fecha_inicio_gestion and self.fecha_fin_gestion:
            if self.fecha_fin_gestion < self.fecha_inicio_gestion:
                raise ValidationError({
                    'fecha_fin_gestion': "La fecha de finalización no puede ser anterior a la fecha de inicio"
                })

        # Teléfono válido
        if self.telefono_contacto_empresarial:
            if not self.telefono_contacto_empresarial.isdigit():
                raise ValidationError({
                    'telefono_contacto_empresarial': "El teléfono debe contener solo números"
                })
            if len(self.telefono_contacto_empresarial) > 10:
                raise ValidationError({
                    'telefono_contacto_empresarial': "El teléfono no puede tener más de 10 números"
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



# ------------------------------------------------------------------------------------------------------------------------------------

# Tabla de Reconocimientos
class Reconocimientos(models.Model):

    # ================= RELACIÓN =================
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='reconocimientos',
        verbose_name="Perfil al que pertenece"
    )

    # ================= TIPO =================
    TIPO_RECONOCIMIENTO_CHOICES = [
        ('Académico', 'Académico'),
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]

    tiporeconocimiento = models.CharField(
        max_length=100,
        choices=TIPO_RECONOCIMIENTO_CHOICES,
        verbose_name="Tipo de reconocimiento"
    )

    # ================= FECHA =================
    fechareconocimiento = models.DateField(
        verbose_name="Fecha del reconocimiento"
    )

    # ================= DESCRIPCIÓN =================
    descripcionreconocimiento = models.TextField(
        blank=True,
        verbose_name="Descripción del reconocimiento"
    )

    # ================= ENTIDAD =================
    entidadpatrocinadora = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Entidad patrocinadora"
    )

    nombrecontactoauspicia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nombre del contacto que auspicia"
    )

    telefonocontactoauspicia = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name="Teléfono del contacto que auspicia"
    )

    # ================= CERTIFICADO =================
    certificado = CloudinaryField(
        'certificado',
        resource_type='raw',
        folder='certificados/reconocimientos',
        blank=True,
        null=True
    )

    imagen_certificado = CloudinaryField(
        'Imagen del certificado',
        resource_type='image',
        folder='certificados/reconocimientos',
        blank=True,
        null=True
    )

    # ================= VISIBILIDAD =================
    activar_para_front = models.BooleanField(
        default=True,
        verbose_name="Mostrar en la página web"
    )

    # ================= CONFIGURACIÓN =================
    class Meta:
        verbose_name = "Reconocimiento"
        verbose_name_plural = "Reconocimientos"
        ordering = ['-fechareconocimiento']

    # ================= VALIDACIONES =================
    def clean(self):
        today = date.today()

        # Fecha no futura
        if self.fechareconocimiento and self.fechareconocimiento > today:
            raise ValidationError({
                'fechareconocimiento': "La fecha del reconocimiento no puede ser futura."
            })

        # Teléfono válido
        if self.telefonocontactoauspicia:
            if not self.telefonocontactoauspicia.isdigit():
                raise ValidationError({
                    'telefonocontactoauspicia': "El teléfono debe contener solo números"
                })
            if len(self.telefonocontactoauspicia) != 10:
                raise ValidationError({
                    'telefonocontactoauspicia': "El teléfono debe tener exactamente 10 dígitos"
                })




# ------------------------------------------------------------------------------------------------------------------------------------

# Tabla Cursos Realizados
class CursosRealizados(models.Model):

    # ================= RELACIÓN CON PERFIL =================
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='cursos_realizados',
        verbose_name="Perfil al que pertenece"
    )

    # ================= DATOS DEL CURSO =================
    nombrecurso = models.CharField(
        max_length=100,
        verbose_name="Nombre del curso"
    )

    fechainicio = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de inicio"
    )

    fechafin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de finalización"
    )

    totalhoras = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        verbose_name="Total de horas"
    )

    descripcioncurso = models.TextField(
        blank=True,
        verbose_name="Descripción del curso"
    )

    # ================= ENTIDAD PATROCINADORA =================
    entidadpatrocinadora = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Entidad patrocinadora"
    )

    nombrecontactoauspicia = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nombre del contacto que auspicia"
    )

    telefonocontactoauspicia = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Teléfono del contacto"
    )

    emailempresapatrocinadora = models.EmailField(
        blank=True,
        verbose_name="Email de la entidad patrocinadora"
    )

    # ================= CERTIFICADO =================
    certificado = CloudinaryField(
        'certificado',
        resource_type='raw',
        folder='certificados/cursos',
        blank=True,
        null=True
    )

    imagen_certificado = CloudinaryField(
        'Imagen del certificado',
        resource_type='image',
        folder='certificados/cursos',
        blank=True,
        null=True
    )

    # ================= VISIBILIDAD =================
    activar_para_front = models.BooleanField(
        default=True,
        verbose_name="Mostrar en la página web"
    )

    # ================= CONFIGURACIÓN =================
    class Meta:
        verbose_name = "Curso realizado"
        verbose_name_plural = "Cursos realizados"
        ordering = ['-fechainicio']

    # ================= VALIDACIONES =================
    def clean(self):
        super().clean()

        # Fecha inicio no futura
        if self.fechainicio and self.fechainicio > timezone.now().date():
            raise ValidationError({
                'fechainicio': "La fecha de inicio no puede ser futura."
            })

        # Fecha fin no anterior a inicio
        if self.fechainicio and self.fechafin:
            if self.fechafin < self.fechainicio:
                raise ValidationError({
                    'fechafin': "La fecha de finalización no puede ser anterior a la fecha de inicio."
                })

        # Teléfono válido
        if self.telefonocontactoauspicia:
            if not self.telefonocontactoauspicia.isdigit():
                raise ValidationError({
                    'telefonocontactoauspicia': "El teléfono debe contener solo números"
                })
            if len(self.telefonocontactoauspicia) != 10:
                raise ValidationError({
                    'telefonocontactoauspicia': "El teléfono debe tener exactamente 10 dígitos"
                })


# ------------------------------------------------------------------------------------------------------------------------------------
# Tabla de Productos Académicos

class ProductosAcademicos(models.Model):

    # Relación con DatosPersonales
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='productos_academicos',
        verbose_name="Perfil al que pertenece"
    )

    nombrerecurso = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nombre del recurso"
    )

    clasificador = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Clasificador"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

        #PARA QUE SE PUEDA AGREGAR UNA FOTO
    imagen = CloudinaryField(
        folder='productos_academicos',  
        null=True,
        blank=True,
        verbose_name="Imagen del producto"
    )

    activar_para_front = models.BooleanField(
        default=True,
        verbose_name="Mostrar en la página"
    )


    class Meta:
        verbose_name = "Producto académico"
        verbose_name_plural = "Productos académicos"


    def __str__(self):
        return self.nombrerecurso or "Producto académico"
    


# ------------------------------------------------------------------------------------------------------------------------------------
# Tabla de Productos Laborales
class ProductosLaborales(models.Model):

    # Relación con DatosPersonales
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='productos_laborales',
        verbose_name="Perfil al que pertenece"
    )

    nombreproducto = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nombre del producto"
    )

    tipoproducto = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Tipo de producto"
    )
    
    fecha_producto = models.DateField(
        verbose_name="Fecha de creación del producto"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    activar_para_front = models.BooleanField(
        default=True,
        verbose_name="Mostrar en la página"
    )

    class Meta:
        verbose_name = "Producto laboral"
        verbose_name_plural = "Productos laborales"
        ordering = ['-fecha_producto']

    def clean(self):
        super().clean()

        # ✔️ Validar SOLO si la fecha existe
        if self.fecha_producto and self.fecha_producto > timezone.now().date():
            raise ValidationError({
                'fecha_producto': "La fecha del producto no puede ser futura."
            })

    def __str__(self):
        return self.nombreproducto or "Producto laboral"



# ------------------------------------------------------------------
# Tabla de Venta Garage

class VentaGarage(models.Model):

    ESTADO_PRODUCTO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]

    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='venta_garage',
        verbose_name="Perfil al que pertenece"
    )

    nombreproducto = models.CharField(
        max_length=100,
        verbose_name="Nombre del producto"
    )

    estadoproducto = models.CharField(
        max_length=40,
        choices=ESTADO_PRODUCTO_CHOICES,
        verbose_name="Estado del producto"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    valordelbien = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        verbose_name="Valor del bien"
    )

    imagen = CloudinaryField(
        folder='venta_garage',
        blank=True,
        null=True,
        verbose_name="Imagen del producto"
    )

    activar_para_front = models.BooleanField(
        default=True,
        verbose_name="Mostrar en la página"
    )

    # ================= FECHA DE PUBLICACIÓN =================
    fecha_publicacion = models.DateField(
        auto_now_add=True,
        verbose_name="Fecha de publicación"
    )

    class Meta:
        verbose_name = "Venta de garage"
        verbose_name_plural = "Venta de garage"
        ordering = ['-fecha_publicacion']  # Los más recientes primero

    def __str__(self):
        return self.nombreproducto or "Venta Garage"
