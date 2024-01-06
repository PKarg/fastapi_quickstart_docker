from celery import Celery

from run.config import project_settings

app = Celery('worker',
             broker=f'redis://:{project_settings.redis.redis_password.get_secret_value()}@{project_settings.redis.redis_host}:'
                    f'{project_settings.redis.redis_port}/{project_settings.redis.redis_db}',
             backend=f'redis://:{project_settings.redis.redis_password.get_secret_value()}@{project_settings.redis.redis_host}:'
                     f'{project_settings.redis.redis_port}/{project_settings.redis.redis_db}')


@app.task(name="add-two-numbers")
def add(x, y):
    return x + y


app.autodiscover_tasks(force=True, related_name="shared_tasks")

if __name__ == "__main__":
    pass
