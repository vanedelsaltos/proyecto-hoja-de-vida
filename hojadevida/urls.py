from django.urls import path
from . import views

urlpatterns = [
    # pantalla inicial (elige ver o administrar) -------------------------------------------
    path('', views.home, name='home'),               # ← inicio público

    # pública-------------------------------------------------------------------------------
    # ver hoja de vida
    path('publico/inicio/', views.publico_inicio, name='publico_inicio'),
    path('publico/inicio/', views.publico_inicio, name='publico'),  # ← línea agregada para home.html
    path('publico/datos/', views.publico_datos, name='publico_datos'),
    path('publico/experiencia/', views.publico_experiencia, name='publico_experiencia'),
    path('publico/cursos/', views.publico_cursos, name='publico_cursos'),
    path('publico/reconocimientos/', views.publico_reconocimientos, name='publico_reconocimientos'),
    path('publico/productos_academicos/', views.publico_productos_academicos, name='publico_productos_academicos'),
    path('publico/productos_laborales/', views.publico_productos_laborales, name='publico_productos_laborales'),
    path('publico/venta_garage/', views.publico_venta_garage, name='publico_venta_garage'),


    # admin---------------------------------------------------------------------------------
    path('inicio/', views.inicio, name='inicio_admin'), # ← admin privado


    # perfiles / esta relacionado con los datos personales -------------------------------------------------------------------------------
    path('datos/', views.lista_perfiles, name='lista_perfiles'),
    path('datos/crear/', views.crear_perfil, name='crear_perfil'),
    path('datos/editar/<int:perfil_id>/', views.editar_perfil, name='editar_perfil'),
    path('datos/activar/<int:perfil_id>/', views.activar_perfil, name='activar_perfil'),
    path('datos/eliminar/<int:perfil_id>/', views.eliminar_perfil, name='eliminar_perfil'),

    #----------------------------------------------------------------------------------------


    #experiencia laboral---------------------------------------------------------------------
    path('experiencia/', views.experiencia, name='experiencia'),
    path('experiencia/crear/', views.crear_experiencia, name='crear_experiencia'),
    path('experiencia/editar/<int:experiencia_id>/', views.editar_experiencia, name='editar_experiencia'),
    path('experiencia/eliminar/<int:experiencia_id>/', views.eliminar_experiencia, name='eliminar_experiencia'),
    #----------------------------------------------------------------------------------------


    #cursos relaizados---------------------------------------------------------------------
    path('cursos/', views.cursos_realizados, name='cursos_realizados'),
    path('cursos/crear/', views.crear_curso, name='crear_curso'),
    path('cursos/editar/<int:curso_id>/', views.editar_curso, name='editar_curso'),
    path('cursos/eliminar/<int:curso_id>/', views.eliminar_curso, name='eliminar_curso'),
    #----------------------------------------------------------------------------------------


    #reconocimientos-------------------------------------------------------------------------
    path('reconocimientos/', views.reconocimientos_lista, name='reconocimientos_lista'),
    path('reconocimientos/crear/', views.crear_reconocimiento, name='crear_reconocimiento'),
    path('reconocimientos/editar/<int:reconocimiento_id>/', views.editar_reconocimiento, name='editar_reconocimiento'),
    path('reconocimientos/eliminar/<int:reconocimiento_id>/', views.eliminar_reconocimiento, name='eliminar_reconocimiento'),
    #----------------------------------------------------------------------------------------


    #productos académicos-------------------------------------------------------------------------
    path('productos_academicos/', views.productos_academicos, name='productos_academicos'),
    path('productos_academicos/crear/', views.crear_producto_academico, name='crear_producto_academico'),
    path('productos_academicos/editar/<int:producto_id>/', views.editar_producto_academico, name='editar_producto_academico'),
    path('productos_academicos/eliminar/<int:producto_id>/', views.eliminar_producto_academico, name='eliminar_producto_academico'),
    #----------------------------------------------------------------------------------------


    #productos laborales-------------------------------------------------------------------------
    path('productos_laborales/', views.productos_laborales, name='productos_laborales'),
    path('productos_laborales/crear/', views.crear_producto_laboral, name='crear_producto_laboral'),
    path('productos_laborales/editar/<int:producto_id>/', views.editar_producto_laboral, name='editar_producto_laboral'),
    path('productos_laborales/eliminar/<int:producto_id>/', views.eliminar_producto_laboral, name='eliminar_producto_laboral'),
    #----------------------------------------------------------------------------------------


    #ventas garage-------------------------------------------------------------------------
    path('venta_garage/', views.venta_garage, name='venta_garage'),
    path('venta_garage/crear/', views.crear_venta_garage, name='crear_venta_garage'),
    path('venta_garage/editar/<int:venta_id>/', views.editar_venta_garage, name='editar_venta_garage'),
    path('venta_garage/eliminar/<int:venta_id>/', views.eliminar_venta_garage, name='eliminar_venta_garage'),
    #----------------------------------------------------------------------------------------



    #Para imprimir hoja de vida
    path(
        'hoja_de_vida/imprimir/',
        views.imprimir_hoja_de_vida,
        name='imprimir_hoja_de_vida'
    ),


]
