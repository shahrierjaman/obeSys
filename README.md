# OBE Software

A Django-based **Outcome-Based Education (OBE) management system** for academic institutions. It helps program controllers define program mission/vision, Program Educational Objectives (PEOs), Program Learning Outcomes (PLOs), map PEOs to PLOs, manage courses, track cohorts, and support instructors in mapping course outcomes back to program-level outcomes.

> ⚠️ **Status: Work in progress.** Views and templates for the core workflows are built, but the data layer (Django models) is not implemented yet — the app currently runs on in-memory demo data defined directly in `views.py`. See [Project Status](#-project-status) below.

---

## ✨ Features (in progress)

- **Program management** — define program mission & vision, PEOs, PLOs, and the PEO–PLO mapping matrix, with version history tracked per change
- **Course management** — create and edit courses, map courses to programs
- **Cohort management** — create cohorts, bulk-upload students via Excel, manage sections
- **Instructor dashboard** — multi-tab view for course offerings (attendance, assessments, outcome mapping, etc.)
- **Rich text editing** — built-in WYSIWYG editor for objective/outcome descriptions, no external editor library required
- **PLO import presets** — quick-import PLOs from ABET / BAETE accreditation templates

---

## 🏗️ Project Structure

```text
obe_software/                       # Project root
│
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
│
├── obe_software/                   # Project configuration package
│   ├── __init__.py
│   ├── settings.py                 # INSTALLED_APPS, database, static files, etc.
│   ├── urls.py                     # Root URL dispatcher (includes core.urls)
│   ├── asgi.py
│   └── wsgi.py
│
└── core/                           # Main application
    ├── __init__.py
    ├── admin.py                    # Django admin registration
    ├── apps.py                     # App configuration
    ├── models.py                   # Database models (not yet implemented)
    ├── views.py                    # All view functions (26+ views)
    ├── urls.py                     # All URL routes (30+ routes)
    │
    └── templates/
        ├── base.html                    # Master layout (sidebar navigation)
        │
        ├── registration/
        │   └── login.html               # Login page (template only — auth not wired up yet)
        │
        ├── program_list.html            # Program list
        ├── program_form.html            # Create a new program (rich text editor)
        ├── program_edit.html            # Edit an existing program (versioned, with change comments)
        │
        ├── course_list.html             # Course list
        ├── course_form.html             # Create/edit a course
        ├── course_mapping.html          # Program–course mapping (drag & drop)
        │
        ├── cohort_list.html             # Cohort list
        ├── cohort_form.html             # Create a cohort
        ├── cohort_detail.html           # Cohort detail (enrolled students)
        ├── cohort_upload.html           # Bulk student upload (Excel)
        ├── cohort_sections.html         # Section management
        │
        ├── offering_detail.html         # Instructor view of a course offering (multi-tab)
        └── instructor_dashboard.html    # Instructor's main dashboard
```

`core` is intentionally the only app for now — it holds every view and template while the data model is still being designed. As the models layer is added, parts of this may be split into focused apps (e.g. `programs`, `courses`, `cohorts`).

---

## 🚀 Getting Started

These steps will get a copy of the project running locally for development.

### Prerequisites

- Python 3.9+
- [pipenv](https://pipenv.pypa.io/) (recommended) — install with `pip install pipenv`
- Firebase project with Firestore database configured
- Service account JSON key from Firebase

### 1. Clone the repository

```bash
git clone https://github.com/shahrierjaman/obeSys.git
cd obeSys
```

### 2. Set up environment variables

Copy `.env.example` to `.env` and fill in your Firebase credentials:

```bash
cp .env.example .env
```

Then edit `.env` and add:
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Firebase service account JSON key
- `FIREBASE_PROJECT_ID`: Your Firebase project ID
- `FIREBASE_DATABASE_ID`: Your Firestore database ID (e.g., `obesys2026`)

**Example:**
```
GOOGLE_APPLICATION_CREDENTIALS=/Users/jahinabid/Downloads/obesity-firebase-adminsdk-fbsvc-xyz.json
FIREBASE_PROJECT_ID=obesity-3e39d
FIREBASE_DATABASE_ID=obesity2026
```

### 3. Install dependencies with pipenv

```bash
pipenv install
```

This reads `Pipfile` and creates a `.venv` virtual environment.

Activate the environment:
```bash
pipenv shell
```

Or, run commands inside it without activating:
```bash
pipenv run python manage.py runserver
```

### 4. Apply migrations

> The app currently has no custom models, so this only sets up Django's built-in tables (auth, sessions, admin).

```bash
python manage.py migrate
```

### 5. (Optional) Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

---

## 📊 Project Status

This project is under active development. Here's where things currently stand:

| Layer | Status |
|---|---|
| URL routing | ✅ Implemented (`core/urls.py`) |
| Views | ✅ Implemented, powered by Firestore backend (`core/firestore_service.py`) |
| Templates | ✅ Implemented for all core workflows listed above |
| Firestore backend | ✅ Configured with Firebase Admin SDK |
| Database models | ⚠️ Not yet implemented (`core/models.py` is a placeholder) |
| Authentication | ⚠️ Login template exists; auth logic is not wired up yet |
| Persistence | ⚠️ Forms currently do not save to a database — submissions are not yet persisted |

**Data layer update:** Program data is now stored in Google Cloud Firestore, with demo programs automatically seeded on initialization. The `core/firestore_service.py` module provides helpers for CRUD operations on programs and other entities.

### Planned next steps

- [ ] Design and implement `core/models.py` (Program, PEO, PLO, Course, Cohort, Student, ProgramVersion, etc.)
- [ ] Wire up form persistence for program create/edit
- [ ] Wire up authentication and role-based access (Dean / Program Controller / Instructor)
- [ ] Persist form submissions (course mapping, cohort upload)
- [ ] Add automated tests

---

## 🧰 Tech Stack

- **Backend:** Django
- **Frontend:** Django Templates + Tailwind CSS (via CDN) + vanilla JavaScript
- **Excel handling:** openpyxl (for cohort student bulk-upload)
- **Database:** Not finalized yet — SQLite is used by default during development; production database TBD

---

## 🤝 Contributing

This project is in an early, fast-changing stage. If you'd like to contribute, please open an issue first to discuss what you'd like to change, especially around the data model, since it's still being designed.

---

## 📄 License

No license has been chosen yet for this project.
