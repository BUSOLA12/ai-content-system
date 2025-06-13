from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_content_system.settings')

app = Celery('ai_content_system')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'