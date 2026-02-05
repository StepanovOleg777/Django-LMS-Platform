import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Загружаем расписание задач
app.conf.beat_schedule = {
    "block-inactive-users-monthly": {
        "task": "materials.tasks.block_inactive_users",
        "schedule": crontab(
            day_of_month="1", hour=0, minute=0
        ),  # 1 числа каждого месяца
        "args": (),
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
