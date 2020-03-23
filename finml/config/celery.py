import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_app = Celery('finml')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

# @celery_app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     from apps.trade.tasks import stock_query, test
#     sender.add_periodic_task(1.0, stock_query())
#     sender.add_periodic_task(2.0, test())

if __name__ == '__main__':
    celery_app.start()
