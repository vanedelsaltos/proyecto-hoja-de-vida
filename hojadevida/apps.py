from django.apps import AppConfig
from django.conf import settings

class HojadevidaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hojadevida'

    def ready(self):
        # Este código se ejecuta cuando la app arranca
        import django
        django.setup()
        from django.contrib.auth.models import User

        # Cambia estos datos por los que quieras
        SUPERUSER_USERNAME = 'vane'
        SUPERUSER_EMAIL = 'vanedelsaltos@gmail.com'
        SUPERUSER_PASSWORD = 'vane1971'

        # Crear superusuario solo si no existe
        if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
            print("Creando superusuario automáticamente...")
            User.objects.create_superuser(
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASSWORD
            )
