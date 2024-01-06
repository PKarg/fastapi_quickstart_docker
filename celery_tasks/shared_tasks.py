from celery import shared_task


@shared_task(name="add-three-numbers")
def add_three(x, y, z):
    return x + y + z


@shared_task(name="add-four-numbers")
def add_four(x, y, z, a):
    return x + y + z + a
