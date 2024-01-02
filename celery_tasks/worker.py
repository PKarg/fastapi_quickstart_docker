import os

from celery import Celery

from run.config import project_settings

os.environ["ENVIRONMENT"] = "test"

app = Celery('worker',
             broker=f'redis://:{project_settings.redis.redis_password.get_secret_value()}@{project_settings.redis.redis_host}:'
                    f'{project_settings.redis.redis_port}/{project_settings.redis.redis_db}',
             backend=f'redis://:{project_settings.redis.redis_password.get_secret_value()}@{project_settings.redis.redis_host}:'
                     f'{project_settings.redis.redis_port}/{project_settings.redis.redis_db}')

print(f'redis://:{project_settings.redis.redis_password}@{project_settings.redis.redis_host}:'
      f'{project_settings.redis.redis_port}/{project_settings.redis.redis_db}')


@app.task
def add(x, y):
    return x + y


if __name__ == "__main__":
    task = add.delay(4, 4)
    print(task)
    res = add.AsyncResult(task.id)
