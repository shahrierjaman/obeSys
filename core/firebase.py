import os

from decouple import config
from firebase_admin import credentials, db, initialize_app

_FIREBASE_APP = None


def get_firebase_app():
    global _FIREBASE_APP
    if _FIREBASE_APP is not None:
        return _FIREBASE_APP

    service_account_path = config('GOOGLE_APPLICATION_CREDENTIALS', default=None)
    database_url = config('FIREBASE_DATABASE_URL', default=None)

    if not service_account_path or not database_url or not os.path.exists(service_account_path):
        _FIREBASE_APP = False
        return None

    try:
        cred = credentials.Certificate(service_account_path)
        options = {'databaseURL': database_url}
        _FIREBASE_APP = initialize_app(cred, options=options)
    except Exception:
        _FIREBASE_APP = False
        return None

    return _FIREBASE_APP


def get_realtime_db():
    app = get_firebase_app()
    if not app:
        return None
    return db.reference('/', app=app)
