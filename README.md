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

- Python 3.10+
- pip
- (Optional) a virtual environment tool — `venv` is built into Python and used below

### 1. Clone the repository

```bash
git clone https://github.com/shahrierjaman/obeSys.git
cd obe_software
```

### 2. Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
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
| Views | ✅ Implemented, currently powered by in-memory demo data in `views.py` |
| Templates | ✅ Implemented for all core workflows listed above |
| Database models | ⚠️ Not yet implemented (`core/models.py` is a placeholder) |
| Authentication | ⚠️ Login template exists; auth logic is not wired up yet |
| Persistence | ⚠️ Forms currently do not save to a database — submissions are not yet persisted |

**What "demo data" means right now:** values like the program list, PEOs/PLOs, cohorts, and version history are hard-coded Python lists/dicts inside `views.py`, clearly marked with comments like `# DEMO DATA — replace with real querysets once the model exists`. This lets the full UI/UX be built and reviewed before the data model is finalized.

### Planned next steps

- [ ] Design and implement `core/models.py` (Program, PEO, PLO, Course, Cohort, Student, ProgramVersion, etc.)
- [ ] Replace demo data in `views.py` with real querysets
- [ ] Wire up authentication and role-based access (Dean / Program Controller / Instructor)
- [ ] Persist form submissions (program create/edit, course mapping, cohort upload)
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
