import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_content_system.settings')

app = Celery('ai_content_system')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):

#     sender.add_periodic_task(
#         21600.0,
#         generate_content_task.s(),
#         name='generate-content-every-6-hours'
#     )