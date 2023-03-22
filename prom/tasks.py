from celery import shared_task


@shared_task
def update_rules(x, y):
    return x + y
