CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json', 'application/x-python-serialize']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SIRIALIZER = 'json'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Etc/UTC'
CELERY_BEAT_SCHEDULE = {}
CELERY_IMPORTS = ('tasks', )