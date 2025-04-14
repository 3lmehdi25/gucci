from django.apps import AppConfig


class GerantDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gerant_dashboard'

    def ready(self):
        import gerant_dashboard.signals