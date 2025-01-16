import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = False

app.conf.beat_schedule = {
    'action_every_30_seconds': {
        'task': 'board.tasks.action',
        'schedule': 30.0,
    },
    'send_weekly_newsletter': {
        'task': 'board.tasks.send_weekly_newsletter',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
}