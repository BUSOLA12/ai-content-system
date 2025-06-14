from django.apps import AppConfig


class ContentGeneratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "content_generator"

    def ready(self):
        import content_generator.signals