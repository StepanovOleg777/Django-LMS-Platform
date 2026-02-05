from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "block-inactive-users-monthly": {
        "task": "materials.tasks.block_inactive_users",
        "schedule": crontab(
            day_of_month="1", hour=0, minute=0
        ),  # 1 числа каждого месяца в 00:00
        "args": (),
        "options": {
            "expires": 30.0,
        },
    },
    "test-task-daily": {
        "task": "materials.tasks.test_celery",
        "schedule": crontab(minute="*/5"),
        "args": (),
    },
}
