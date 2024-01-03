import os

os.environ["ENVIRONMENT"] = "test"

pytest_plugins = ('celery.contrib.pytest',)
