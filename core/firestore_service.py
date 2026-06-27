from datetime import datetime

from .firebase import get_firestore_client

PROGRAM_COLLECTION = 'programs'


def _normalize_program_id(program_id):
    return str(program_id)


def save_program(program_id, payload):
    db = get_firestore_client()
    doc_ref = db.collection(PROGRAM_COLLECTION).document(_normalize_program_id(program_id))
    payload = payload.copy()
    payload['updated_at'] = datetime.utcnow()
    doc_ref.set(payload, merge=True)
    return doc_ref.get().to_dict()


def get_program(program_id):
    db = get_firestore_client()
    doc_ref = db.collection(PROGRAM_COLLECTION).document(_normalize_program_id(program_id))
    snapshot = doc_ref.get()
    return snapshot.to_dict() if snapshot.exists else None


def list_programs():
    db = get_firestore_client()
    docs = db.collection(PROGRAM_COLLECTION).stream()
    return [doc.to_dict() for doc in docs]


def seed_demo_programs():
    programs = [
        {
            'id': 1,
            'code': 'BSCS',
            'name': 'Bachelor of Science in Computer Science',
            'version': 3,
            'status': 'Active',
            'peo_count': 3,
            'plo_count': 12,
            'detail': {
                'inst_vision': 'To be a globally recognized institution advancing knowledge and innovation for the betterment of society.',
                'program_vision': 'To be a leading program producing computer science graduates who innovate and lead in a digital world.',
                'peos': [
                    {'title': 'Professionalism', 'description': 'Graduates will engage in professional practice with integrity, ethics, and respect for diversity.'},
                    {'title': 'Technical Excellence', 'description': 'Graduates will apply advanced computing principles to design and develop robust, scalable software solutions.'},
                    {'title': 'Lifelong Learning', 'description': 'Graduates will pursue continued learning and professional development throughout their careers.'},
                ],
                'plos': [
                    {'title': 'Engineering knowledge', 'description': 'Apply knowledge of computing, mathematics, and science to solve complex computing problems.'},
                    {'title': 'Problem analysis', 'description': 'Identify, formulate, and analyze complex computing problems using first principles.'},
                    {'title': 'Design/development of solutions', 'description': 'Design solutions for complex computing problems and design software systems that meet specified needs.'},
                ],
            },
        },
        {
            'id': 2,
            'code': 'BSEEE',
            'name': 'Bachelor of Science in Electrical & Electronic Engineering',
            'version': 1,
            'status': 'Active',
            'peo_count': 3,
            'plo_count': 10,
        },
    ]

    for program in programs:
        program['created_at'] = datetime.utcnow()
        program['updated_at'] = datetime.utcnow()
        save_program(program['id'], program)

    return programs


def clear_programs():
    db = get_firestore_client()
    docs = db.collection(PROGRAM_COLLECTION).stream()
    for doc in docs:
        db.collection(PROGRAM_COLLECTION).document(doc.id).delete()
