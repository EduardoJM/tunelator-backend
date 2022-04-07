from common.celery import setup_app

celery_app = setup_app('core.settings')
