from contextlib import suppress
import os
from pathlib import Path
import firebase_admin

def setup_firebase():
    APP_DIR = Path(__file__).resolve().parent.parent
    credentials = firebase_admin.credentials.Certificate(
        os.path.join(APP_DIR, "firebase_keys.json")
    )
    with suppress(ValueError):
        firebase_admin.initialize_app(credentials)
