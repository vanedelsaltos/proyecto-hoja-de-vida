from django.apps import AppConfig


class HojadevidaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hojadevida'

    def ready(self):
        from django.contrib.auth.models import User

        SUPERUSER_USERNAME = 'vane'
        SUPERUSER_EMAIL = 'vanedelsaltos@gmail.com'
        SUPERUSER_PASSWORD = 'vane1971'

        if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
            print("Creando superusuario automáticamente...")
            User.objects.create_superuser(
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASSWORD
            )
