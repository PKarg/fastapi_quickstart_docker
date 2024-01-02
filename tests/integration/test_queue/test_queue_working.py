from celery_tasks.worker import add


def test_add_task():
    task = add.delay(4, 4)
    print(task.id)
    print(task.status)
    res = add.AsyncResult(task.id)
    while not res.ready():
        pass
    print(res.get())
    assert res.get() == 8
