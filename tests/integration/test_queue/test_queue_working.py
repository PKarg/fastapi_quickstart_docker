from celery_tasks.worker import add


def test_create_task(celery_app, celery_worker):
    @celery_app.task
    def mul(x, y):
        return x * y

    celery_worker.reload()
    assert mul.delay(4, 4).get(timeout=10) == 16


def test_add_task(celery_register_tasks, celery_session_app, celery_session_worker):
    task = add.delay(4, 4)
    print(task.id)
    print(task.status)
    res = add.AsyncResult(task.id)
    while not res.ready():
        pass
    print(res.get())
    assert res.get() == 8
