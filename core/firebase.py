import os

from firebase_admin import credentials, initialize_app
from google.cloud import firestore
from google.oauth2 import service_account

_FIREBASE_APP = None


def get_firebase_app():
    global _FIREBASE_APP
    if _FIREBASE_APP:
        return _FIREBASE_APP

    service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not service_account_path:
        raise RuntimeError(
            'Firebase service account not configured. Set GOOGLE_APPLICATION_CREDENTIALS to the JSON key file path.'
        )
    if not os.path.exists(service_account_path):
        raise RuntimeError(
            f'Firebase service account file not found: {service_account_path}'
        )

    cred = credentials.Certificate(service_account_path)
    project_id = os.getenv('FIREBASE_PROJECT_ID')
    options = {'projectId': project_id} if project_id else None
    _FIREBASE_APP = initialize_app(cred, options=options)
    return _FIREBASE_APP


def get_firestore_client():
    service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not service_account_path:
        raise RuntimeError(
            'Firebase service account not configured. Set GOOGLE_APPLICATION_CREDENTIALS to the JSON key file path.'
        )

    project_id = os.getenv('FIREBASE_PROJECT_ID')
    if not project_id:
        raise RuntimeError('Firebase project ID is not configured. Set FIREBASE_PROJECT_ID.')

    database_id = os.getenv('FIREBASE_DATABASE_ID', '(default)')
    if database_id == '(default)':
        database = database_id
    elif database_id.startswith('projects/') and '/databases/' in database_id:
        database = database_id.split('/databases/')[-1]
    else:
        database = database_id

    creds = service_account.Credentials.from_service_account_file(service_account_path)
    return firestore.Client(project=project_id, credentials=creds, database=database)
