from celery import shared_task


@shared_task(name="add-three-numbers")
def add_three(x, y, z):
    return x + y + z
