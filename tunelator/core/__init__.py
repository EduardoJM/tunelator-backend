from common.celery import setup_app
from common.firebase import setup_firebase

celery_app = setup_app('core.settings')
setup_firebase()
