from datetime import date

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect


DEMO_PROGRAMS = [
    {'id': 1, 'code': 'BSCS', 'name': 'Bachelor of Science in Computer Science', 'version': 3, 'status': 'Active', 'peo_count': 3, 'plo_count': 12},
    {'id': 2, 'code': 'BSEEE', 'name': 'Bachelor of Science in Electrical & Electronic Engineering', 'version': 1, 'status': 'Active', 'peo_count': 3, 'plo_count': 10},
    {'id': 3, 'code': 'BSCE', 'name': 'Bachelor of Science in Civil Engineering', 'version': 1, 'status': 'Draft', 'peo_count': 2, 'plo_count': 8},
    {'id': 4, 'code': 'BBA', 'name': 'Bachelor of Business Administration', 'version': 2, 'status': 'Archived', 'peo_count': 4, 'plo_count': 11},
    # Assigned by the Dean but not yet opened/configured by the controller (v0)
    {'id': 5, 'code': 'BSME', 'name': 'Bachelor of Science in Mechanical Engineering', 'version': 0, 'status': 'New', 'peo_count': 0, 'plo_count': 0},
    {'id': 6, 'code': 'BSIT', 'name': 'Bachelor of Science in Information Technology', 'version': 0, 'status': 'New', 'peo_count': 0, 'plo_count': 0},
]

RECENT_ACTIVITY = [
    {'icon': 'fa-link', 'color': 'indigo', 'text': 'Updated PEO-PLO mapping for BSCS.', 'time': '2 hours ago'},
    {'icon': 'fa-user-tie', 'color': 'amber', 'text': 'Dean assigned a new program: BSIT.', 'time': '1 day ago'},
    {'icon': 'fa-bullseye', 'color': 'emerald', 'text': 'Added 2 PEOs to BSEEE.', 'time': '3 days ago'},
    {'icon': 'fa-file-import', 'color': 'sky', 'text': 'Imported the ABET PLO preset for BSCE.', 'time': '5 days ago'},
    {'icon': 'fa-archive', 'color': 'slate', 'text': 'Archived an older version of BBA.', 'time': '1 week ago'},
]


# ----------------------------------------------------------------------------
# DEMO PROGRAM DETAIL — the full configured content for a program that has
# already been managed at least once (version >= 1). Replace with real
# related-model lookups once Mission / PEO / PLO / Mapping / AssessmentTool
# models exist, e.g.:
#     program.missions.filter(scope='institution')
#     program.peos.order_by('order')
# Keyed by program id. Programs not present here (e.g. v0 / brand new ones)
# simply have nothing to prefill — program_edit should not be reachable for
# those (they use "Manage", i.e. program_create, instead).
# ----------------------------------------------------------------------------
DEMO_PROGRAM_DETAIL = {
    1: {  # BSCS
        'inst_vision': 'To be a globally recognized institution advancing knowledge and innovation for the betterment of society.',
        'inst_missions': [
            'To advance knowledge through excellence in teaching and research.',
            'To cultivate ethical, socially responsible leaders.',
        ],
        'program_vision': 'To be a leading program producing computer science graduates who innovate and lead in a digital world.',
        'program_missions': [
            'To provide a rigorous, industry-relevant computing curriculum.',
            'To foster research and innovation in emerging technologies.',
            'To instill professional and ethical responsibility in graduates.',
        ],
        'peos': [
            {
                'title': 'Professionalism',
                'description': 'Graduates will engage in professional practice with integrity, ethics, and respect for diversity.',
            },
            {
                'title': 'Technical Excellence',
                'description': 'Graduates will apply advanced computing principles to design and develop robust, scalable software solutions.',
            },
            {
                'title': 'Lifelong Learning',
                'description': 'Graduates will pursue continued learning and professional development throughout their careers.',
            },
        ],
        'plos': [
            {'title': 'Engineering knowledge', 'description': 'Apply knowledge of computing, mathematics, and science to solve complex computing problems.'},
            {'title': 'Problem analysis', 'description': 'Identify, formulate, and analyze complex computing problems using first principles.'},
            {'title': 'Design/development of solutions', 'description': 'Design solutions for complex computing problems and design software systems that meet specified needs.'},
            {'title': 'Modern tool usage', 'description': 'Create, select, and apply appropriate techniques, resources, and modern computing tools.'},
            {'title': 'Communication', 'description': 'Communicate effectively on complex computing activities with the community and society at large.'},
            {'title': 'Ethics', 'description': 'Apply ethical principles and commit to professional ethics and responsibilities of computing practice.'},
        ],
        # mapping[peo_index][plo_index] = bool, aligned positionally with peos/plos above
        'mapping': [
            [True, True, False, False, True, True],
            [True, True, True, True, False, False],
            [False, False, True, True, True, False],
        ],
        'assessment_tools': ['Quiz', 'Midterm', 'Final Project', 'Presentation'],
        'assessment_tools_custom': ['Capstone Defense'],
        'version_history': [
            {
                'version': 3,
                'date': 'May 14, 2026',
                'editor': 'Dr. Farhan Ahmed',
                'sections_changed': ['PLOs', 'PEO-PLO Mapping'],
                'comments': {
                    'PLOs': 'Updated wording on Modern Tool Usage to match latest ABET descriptor.',
                    'PEO-PLO Mapping': 'Re-mapped PLO 4 and 6 after PLO wording update.',
                },
            },
            {
                'version': 2,
                'date': 'Nov 02, 2025',
                'editor': 'Dr. Farhan Ahmed',
                'sections_changed': ['Mission & Vision', 'Settings & Assessment Tools'],
                'comments': {
                    'Mission & Vision': 'Revised program mission to reflect new research focus areas.',
                    'Settings & Assessment Tools': 'Added Capstone Defense as a recurring assessment tool.',
                },
            },
            {
                'version': 1,
                'date': 'Mar 20, 2025',
                'editor': 'Dr. Farhan Ahmed',
                'sections_changed': ['Mission & Vision', 'PEOs', 'PLOs', 'PEO-PLO Mapping', 'Settings & Assessment Tools'],
                'comments': {
                    'Mission & Vision': 'Initial setup based on department curriculum committee draft.',
                    'PEOs': 'Initial PEOs adapted from outgoing curriculum.',
                    'PLOs': 'Imported ABET preset and adjusted wording for local context.',
                    'PEO-PLO Mapping': 'Initial mapping drafted with curriculum committee.',
                    'Settings & Assessment Tools': 'Initial assessment tools selected.',
                },
            },
        ],
    },
    2: {  # BSEEE
        'inst_vision': 'To be a globally recognized institution advancing knowledge and innovation for the betterment of society.',
        'inst_missions': [
            'To advance knowledge through excellence in teaching and research.',
        ],
        'program_vision': 'To be a recognized leader in electrical and electronic engineering education and innovation.',
        'program_missions': [
            'To deliver a strong foundation in electrical and electronic engineering principles.',
            'To prepare graduates for industry, research, and entrepreneurship.',
        ],
        'peos': [
            {'title': 'Technical Competence', 'description': 'Graduates will apply electrical and electronic engineering principles to solve real-world problems.'},
            {'title': 'Professional Growth', 'description': 'Graduates will pursue continued professional development and leadership roles.'},
            {'title': 'Societal Impact', 'description': 'Graduates will contribute engineering solutions that benefit society and the environment.'},
        ],
        'plos': [
            {'title': 'Engineering knowledge', 'description': 'Apply knowledge of mathematics, science, and engineering fundamentals to electrical and electronic systems.'},
            {'title': 'Design/development of solutions', 'description': 'Design electrical and electronic systems that meet specified needs.'},
            {'title': 'Modern tool usage', 'description': 'Apply modern engineering and IT tools to electrical engineering activities.'},
            {'title': 'Ethics', 'description': 'Apply ethical principles in engineering practice.'},
            {'title': 'Communication', 'description': 'Communicate effectively with technical and non-technical audiences.'},
        ],
        'mapping': [
            [True, True, True, False, False],
            [False, True, True, True, False],
            [True, False, False, True, True],
        ],
        'assessment_tools': ['Quiz', 'Midterm', 'Lab Report', 'Practical Exam'],
        'assessment_tools_custom': [],
        'version_history': [
            {
                'version': 1,
                'date': 'Jan 18, 2026',
                'editor': 'Dr. Nusrat Jahan',
                'sections_changed': ['Mission & Vision', 'PEOs', 'PLOs', 'PEO-PLO Mapping', 'Settings & Assessment Tools'],
                'comments': {
                    'Mission & Vision': 'Initial program setup.',
                    'PEOs': 'Initial PEOs drafted with department input.',
                    'PLOs': 'Imported BAETE preset.',
                    'PEO-PLO Mapping': 'Initial mapping drafted.',
                    'Settings & Assessment Tools': 'Initial assessment tools selected.',
                },
            },
        ],
    },
}


def dashboard(request):
    """
    Program Controller dashboard.
    Replace the hard-coded numbers/lists with real aggregates once the
    Program / PEO / PLO / ActivityLog models exist, e.g.:
        Program.objects.filter(controller=request.user)
    """
    new_programs = [p for p in DEMO_PROGRAMS if p['version'] == 0]
    managed_programs = [p for p in DEMO_PROGRAMS if p['version'] > 0]

    context = {
        'today': date.today().strftime('%A, %B %d, %Y'),
        'stats': {
            'assigned_programs': len(DEMO_PROGRAMS),
            'peos_defined': sum(p['peo_count'] for p in managed_programs),
            'plos_defined': sum(p['plo_count'] for p in managed_programs),
            'pending_actions': len(new_programs),
        },
        'new_programs': new_programs,
        'recent_activity': RECENT_ACTIVITY,
    }
    return render(request, 'base.html', context)


def program_list(request):
    """
    Shows every program assigned to the logged-in Program Controller.
    Action column: Manage -> program_create (prefilled, locked code/name),
                    Edit   -> program_edit (versioning / full edit page).
    """
    context = {'programs': DEMO_PROGRAMS}
    return render(request, 'program_list.html', context)


def program_create(request):
    context = {
        'program_id': request.GET.get('id', ''),
        'code': request.GET.get('code', ''),
        'name': request.GET.get('name', ''),
    }
    return render(request, 'program_form.html', context)


def program_edit(request, program_id):
    program = next((p for p in DEMO_PROGRAMS if p['id'] == program_id), None)
    if program is None:
        # Real implementation: raise Http404 via get_object_or_404 above.
        return render(request, 'program_list.html', {'programs': DEMO_PROGRAMS, 'error': 'Program not found.'})

    detail = DEMO_PROGRAM_DETAIL.get(program_id, {
        'inst_vision': '',
        'inst_missions': [],
        'program_vision': '',
        'program_missions': [],
        'peos': [],
        'plos': [],
        'mapping': [],
        'assessment_tools': [],
        'assessment_tools_custom': [],
        'version_history': [],
    })

    context = {
        'program_id': program['id'],
        'code': program['code'],
        'name': program['name'],
        'current_version': program['version'],
        'next_version': program['version'] + 1,
        'status': program['status'],
        'detail': detail,
        'standard_assessment_tools': [
            'Quiz', 'Midterm', 'Final Project', 'Lab Report', 'Presentation',
            'Case Study', 'Term Paper', 'Practical Exam', 'Viva / Oral Exam', 'Portfolio',
        ],
    }
    return render(request, 'program_edit.html', context)


def program_update(request, program_id):
    return JsonResponse({'status': 'ok', 'message': 'Update received (demo stub — not yet persisted).'})


# ----------------------------------------------------------------------------
# DEMO PLO presets for the "Import PLOs" dropdown on program_form.html /
# program_edit.html. Move these into the database (e.g. an
# AccreditationBody / PLOPreset model) once accreditation bodies are
# modeled properly.
# ----------------------------------------------------------------------------
PLO_PRESETS = {
    'abet': [
        {
            'title': 'Engineering Problem Solving',
            'description': 'An ability to identify, formulate, and solve complex engineering problems by applying principles of engineering, science, and mathematics.',
        },
        {
            'title': 'Engineering Design',
            'description': 'An ability to apply engineering design to produce solutions that meet specified needs, with consideration of public health, safety, and welfare, as well as global, cultural, social, environmental, and economic factors.',
        },
        {
            'title': 'Communication',
            'description': 'An ability to communicate effectively with a range of audiences.',
        },
        {
            'title': 'Ethical Responsibility',
            'description': 'An ability to recognize ethical and professional responsibilities in engineering situations and make informed judgments, considering the impact of engineering solutions in global, economic, environmental, and societal contexts.',
        },
        {
            'title': 'Teamwork',
            'description': 'An ability to function effectively on a team whose members together provide leadership, create a collaborative and inclusive environment, establish goals, plan tasks, and meet objectives.',
        },
    ],
    'baete': [
        {
            'title': 'Engineering Knowledge',
            'description': 'Apply knowledge of mathematics, natural science, engineering fundamentals, and an engineering specialization to the solution of complex engineering problems.',
        },
        {
            'title': 'Problem Analysis',
            'description': 'Identify, formulate, research literature and analyze complex engineering problems reaching substantiated conclusions using first principles of mathematics, natural sciences, and engineering sciences.',
        },
        {
            'title': 'Design/Development of Solutions',
            'description': 'Design solutions for complex engineering problems and design systems, components, or processes that meet specified needs with appropriate consideration for public health and safety, cultural, societal, and environmental considerations.',
        },
        {
            'title': 'Modern Tool Usage',
            'description': 'Create, select, and apply appropriate techniques, resources, and modern engineering and IT tools, including prediction and modeling, to complex engineering activities.',
        },
        {
            'title': 'The Engineer and Society',
            'description': 'Apply reasoning informed by contextual knowledge to assess societal, health, safety, legal, and cultural issues and the consequent responsibilities relevant to professional engineering practice.',
        },
    ],
}


def plo_preset_import(request, source):
    """
    Returns a demo set of PLOs for the given accreditation source
    ('abet' or 'baete'), used by the "Import PLOs" dropdown.
    """
    data = PLO_PRESETS.get(source.lower(), [])
    return JsonResponse({'source': source, 'plos': data})


def course_list(request):
    # Dummy data for UI demonstration
    courses = [
        {
            'id': 1,
            'code': 'CS-101',
            'name': 'Introduction to Computer Science',
            'credits': 3,
            'version': 2,
            'is_archived': False,
            'programs': ['BSCS', 'BSEE'],
            'created_at': '2024-08-15',
            'has_prerequisites': False,
        },
        {
            'id': 20,
            'code': 'CS-201',
            'name': 'Data Structures and Algorithms',
            'credits': 4,
            'version': 3,
            'is_archived': False,
            'programs': ['BSCS'],
            'created_at': '2024-09-01',
            'has_prerequisites': True,
        },
        {
            'id': 3,
            'code': 'EE-101',
            'name': 'Circuit Analysis',
            'credits': 3,
            'version': 1,
            'is_archived': False,
            'programs': ['BSEE', 'BSME'],
            'created_at': '2024-06-10',
            'has_prerequisites': False,
        },
        {
            'id': 4,
            'code': 'ME-201',
            'name': 'Thermodynamics',
            'credits': 3,
            'version': 2,
            'is_archived': True,
            'programs': ['BSME'],
            'created_at': '2023-11-20',
            'has_prerequisites': True,
        },
        {
            'id': 5,
            'code': 'CS-301',
            'name': 'Database Management Systems',
            'credits': 3,
            'version': 1,
            'is_archived': False,
            'programs': ['BSCS', 'BBA'],
            'created_at': '2025-01-15',
            'has_prerequisites': True,
        },
    ]
    return render(request, 'course_list.html', {'courses': courses})

PROGRAM_NAMES = {
    'BSCS': 'BS Computer Science',
    'BSEE': 'BS Electrical Engineering',
    'BSME': 'BS Mechanical Engineering',
    'BBA': 'BBA - Business Administration',
    'BSPhy': 'BS Physics',
}

PROGRAM_PLOS_DATA = {
    'BSCS': [
        {'id': 1, 'code': 'a', 'title': 'Engineering Knowledge', 'description': 'Apply knowledge of mathematics, natural science, engineering fundamentals and computing to the solution of complex computing problems.'},
        {'id': 2, 'code': 'b', 'title': 'Problem Analysis', 'description': 'Identify, formulate, research literature and analyse complex computing problems reaching substantiated conclusions.'},
        {'id': 3, 'code': 'c', 'title': 'Design/Development of Solutions', 'description': 'Design solutions for complex computing problems and design systems, components or processes that meet specified needs.'},
    ],
    'BSEE': [
        {'id': 1, 'code': 'a', 'title': 'Engineering Knowledge', 'description': 'Apply knowledge of mathematics, science and electrical engineering fundamentals to complex engineering problems.'},
        {'id': 2, 'code': 'b', 'title': 'Investigation', 'description': 'Conduct investigations of complex electrical engineering problems using research-based knowledge.'},
        {'id': 3, 'code': 'c', 'title': 'Modern Tool Usage', 'description': 'Create, select and apply appropriate techniques, resources and modern engineering tools.'},
    ],
    'BSME': [
        {'id': 1, 'code': 'a', 'title': 'Engineering Knowledge', 'description': 'Apply mathematics, science and mechanical engineering fundamentals to the solution of complex mechanical engineering problems.'},
        {'id': 2, 'code': 'b', 'title': 'Design/Development of Solutions', 'description': 'Design mechanical systems or processes that meet specified needs with appropriate consideration for safety.'},
    ],
    'BBA': [
        {'id': 1, 'code': 'a', 'title': 'Business Knowledge', 'description': 'Demonstrate broad knowledge of functional areas of business including finance, marketing and operations.'},
        {'id': 2, 'code': 'b', 'title': 'Ethical Reasoning', 'description': 'Apply ethical reasoning to business decision-making in diverse organizational contexts.'},
    ],
    'BSPhy': [
        {'id': 1, 'code': 'a', 'title': 'Scientific Knowledge', 'description': 'Apply fundamental principles of physics to analyse and solve scientific problems.'},
        {'id': 2, 'code': 'b', 'title': 'Experimental Skills', 'description': 'Design and conduct experiments, and analyse and interpret data.'},
    ],
}


def course_create(request):
    context = {
        'is_edit': False,
        'course': None,
        'all_programs': PROGRAM_NAMES,
        'program_plos': PROGRAM_PLOS_DATA,
    }
    return render(request, 'course_form.html', context)


def course_edit(request, pk):
    # Dummy data for an existing course
    dummy_course = {
        'id': pk,
        'code': 'CS-201',
        'name': 'Data Structures and Algorithms',
        'credits': 4,
        'version': 3,
        'is_archived': False,
        'created_at': '2024-09-01',
        'programs': ['BSCS'],
        'objectives': 'To equip students with fundamental data structures and algorithms essential for software development.',
        'reference_materials': 'Data Structures and Algorithms in Python (Goodrich), Introduction to Algorithms (CLRS)',
        'prerequisites': ['CS-101'],
        'clos': [
            {
                'id': 1,
                'code': 'CLO-1',
                'description': 'Implement fundamental data structures including arrays, linked lists, stacks, and queues.',
                'plo_key': 'BSCS-1',
                'learning_domain': 'Cognitive',
            },
            {
                'id': 2,
                'code': 'CLO-2',
                'description': 'Analyze the time and space complexity of algorithms using Big-O notation.',
                'plo_key': 'BSCS-2',
                'learning_domain': 'Cognitive',
            },
            {
                'id': 3,
                'code': 'CLO-3',
                'description': 'Design efficient algorithms for sorting, searching, and graph traversal.',
                'plo_key': 'BSCS-3',
                'learning_domain': 'Psychomotor',
            },
        ],
    }
    context = {
        'is_edit': True,
        'course': dummy_course,
        'all_programs': PROGRAM_NAMES,
        'program_plos': PROGRAM_PLOS_DATA,
    }
    return render(request, 'course_form.html', context)



def program_mapping(request, pk):
    # Dummy data for the selected program
    program = {
        'id': pk,
        'code': 'BSCS',
        'name': 'Bachelor of Science in Computer Science',
    }
    
    # ALL COURSES IN THE SYSTEM (THIS WAS MISSING BEFORE)
    all_courses = [
        {'id': 1, 'code': 'CS-101', 'name': 'Introduction to Computer Science'},
        {'id': 2, 'code': 'CS-102', 'name': 'Programming Fundamentals'},
        {'id': 3, 'code': 'CS-201', 'name': 'Data Structures and Algorithms'},
        {'id': 4, 'code': 'CS-202', 'name': 'Database Management Systems'},
        {'id': 5, 'code': 'CS-301', 'name': 'Operating Systems'},
        {'id': 6, 'code': 'CS-302', 'name': 'Software Engineering'},
        {'id': 7, 'code': 'CS-401', 'name': 'Artificial Intelligence'},
        {'id': 8, 'code': 'MATH-101', 'name': 'Calculus I'},
        {'id': 9, 'code': 'PHY-101', 'name': 'Physics I'},
        {'id': 10, 'code': 'ENG-101', 'name': 'English Composition'},
    ]
    
    # Courses currently mapped to BSCS (with order)
    mapped_courses = [
        {'id': 2, 'code': 'CS-102', 'name': 'Programming Fundamentals', 'order': 1},
        {'id': 1, 'code': 'CS-101', 'name': 'Introduction to Computer Science', 'order': 2},
        {'id': 3, 'code': 'CS-201', 'name': 'Data Structures and Algorithms', 'order': 3},
        {'id': 4, 'code': 'CS-202', 'name': 'Database Management Systems', 'order': 4},
        {'id': 6, 'code': 'CS-302', 'name': 'Software Engineering', 'order': 5},
    ]
    
    # IDs of mapped courses for filtering the available list
    mapped_ids = [c['id'] for c in mapped_courses]
    
    # Available courses (not mapped to this program)
    available_courses = [c for c in all_courses if c['id'] not in mapped_ids]
    
    context = {
        'program': program,
        'all_courses': all_courses,           # Pass ALL courses to JavaScript
        'available_courses': available_courses,
        'mapped_courses': mapped_courses,
        'mapped_ids': mapped_ids,             # For the JavaScript to initialize mapping status
    }
    return render(request, 'course_mapping.html', context)


def cohort_list(request):
    # Dummy data for cohorts
    cohorts = [
        {
            'id': 1,
            'name': 'Fall 2024',
            'program_code': 'BSCS',
            'program_name': 'Bachelor of Science in Computer Science',
            'start_year': 2024,
            'graduation_year': 2028,
            'student_count': 45,
            'section_count': 2,
            'status': 'Active',
        },
        {
            'id': 2,
            'name': 'Spring 2025',
            'program_code': 'BSEE',
            'program_name': 'Bachelor of Science in Electrical Engineering',
            'start_year': 2025,
            'graduation_year': 2029,
            'student_count': 32,
            'section_count': 1,
            'status': 'Active',
        },
        {
            'id': 3,
            'name': 'Fall 2023',
            'program_code': 'BSME',
            'program_name': 'Bachelor of Science in Mechanical Engineering',
            'start_year': 2023,
            'graduation_year': 2027,
            'student_count': 38,
            'section_count': 2,
            'status': 'Active',
        },
        {
            'id': 4,
            'name': 'Spring 2024',
            'program_code': 'BBA',
            'program_name': 'Bachelor of Business Administration',
            'start_year': 2024,
            'graduation_year': 2028,
            'student_count': 28,
            'section_count': 1,
            'status': 'Archived',
        },
        {
            'id': 5,
            'name': 'Fall 2025',
            'program_code': 'BSCS',
            'program_name': 'Bachelor of Science in Computer Science',
            'start_year': 2025,
            'graduation_year': 2029,
            'student_count': 0,
            'section_count': 0,
            'status': 'Pending',
        },
    ]
    return render(request, 'cohort_list.html', {'cohorts': cohorts})

def cohort_create(request):
    # Empty form for new cohort
    context = {
        'is_edit': False,
        'cohort': None,
    }
    return render(request, 'cohort_form.html', context)

def cohort_edit(request, pk):
    # Dummy data for an existing cohort
    dummy_cohort = {
        'id': pk,
        'name': 'Fall 2024',
        'program_code': 'BSCS',
        'program_name': 'Bachelor of Science in Computer Science',
        'start_year': 2024,
        'graduation_year': 2028,
        'student_count': 45,
        'section_count': 2,
        'status': 'Active',
    }
    context = {
        'is_edit': True,
        'cohort': dummy_cohort,
    }
    return render(request, 'cohort_form.html', context)

def cohort_detail(request, pk):
    # Dummy cohort data
    cohort = {
        'id': pk,
        'name': 'Fall 2024',
        'program_code': 'BSCS',
        'program_name': 'Bachelor of Science in Computer Science',
        'start_year': 2024,
        'graduation_year': 2028,
        'student_count': 45,
        'section_count': 2,
        'status': 'Active',
    }
    
    # Dummy student list for this cohort
    students = [
        {'id': 1, 'student_id': '2024-001', 'name': 'Ahmed Khan', 'email': 'ahmed.khan@university.edu', 'status': 'Active'},
        {'id': 2, 'student_id': '2024-002', 'name': 'Fatima Ali', 'email': 'fatima.ali@university.edu', 'status': 'Active'},
        {'id': 3, 'student_id': '2024-003', 'name': 'Muhammad Usman', 'email': 'm.usman@university.edu', 'status': 'Active'},
        {'id': 4, 'student_id': '2024-004', 'name': 'Ayesha Siddiqui', 'email': 'ayesha.s@university.edu', 'status': 'Active'},
        {'id': 5, 'student_id': '2024-005', 'name': 'Bilal Ahmed', 'email': 'bilal.a@university.edu', 'status': 'Dropped'},
        {'id': 6, 'student_id': '2024-006', 'name': 'Hira Malik', 'email': 'hira.m@university.edu', 'status': 'Active'},
        {'id': 7, 'student_id': '2024-007', 'name': 'Omar Farooq', 'email': 'omar.f@university.edu', 'status': 'Active'},
        {'id': 8, 'student_id': '2024-008', 'name': 'Zara Abbas', 'email': 'zara.a@university.edu', 'status': 'Transferred'},
        {'id': 9, 'student_id': '2024-009', 'name': 'Hassan Raza', 'email': 'hassan.r@university.edu', 'status': 'Active'},
        {'id': 10, 'student_id': '2024-010', 'name': 'Mahnoor Shah', 'email': 'mahnoor.s@university.edu', 'status': 'Active'},
    ]
    
    context = {
        'cohort': cohort,
        'students': students,
    }
    return render(request, 'cohort_detail.html', context)

def cohort_upload(request, pk):
    # Replace this later with actual Cohort model query
    cohort = {
        'id': pk,
        'name': 'Fall 2024',
        'program_code': 'BSCS',
        'program_name': 'Bachelor of Science in Computer Science',
    }

    context = {
        'cohort': cohort,
    }

    return render(request, 'cohort_upload.html', context)

def cohort_sections(request, pk):
    # Cohort details
    cohort = {
        'id': pk,
        'name': 'Fall 2024',
        'program_code': 'BSCS',
        'program_name': 'Bachelor of Science in Computer Science',
        'student_count': 45,
    }
    
    # Dummy sections for this cohort
    sections = [
        {
            'id': 1,
            'name': 'Section A',
            'instructor': 'Dr. Ahmed Khan',
            'student_count': 22,
            'status': 'Active',
        },
        {
            'id': 2,
            'name': 'Section B',
            'instructor': 'Dr. Fatima Ali',
            'student_count': 23,
            'status': 'Active',
        },
        {
            'id': 3,
            'name': 'Section C',
            'instructor': 'Not Assigned',
            'student_count': 0,
            'status': 'Pending',
        },
    ]
    
    # Available instructors (for dropdown)
    instructors = [
        {'id': 1, 'name': 'Dr. Ahmed Khan'},
        {'id': 2, 'name': 'Dr. Fatima Ali'},
        {'id': 3, 'name': 'Dr. Muhammad Usman'},
        {'id': 4, 'name': 'Dr. Ayesha Siddiqui'},
        {'id': 5, 'name': 'Dr. Bilal Ahmed'},
    ]
    
    context = {
        'cohort': cohort,
        'sections': sections,
        'instructors': instructors,
        'total_students': 45,
    }
    return render(request, 'cohort_sections.html', context)


# ==================== OFFERING VIEWS ====================

def offering_list(request):
    # Dummy data for course offerings
    offerings = [
        {
            'id': 1,
            'course_code': 'CS-101',
            'course_name': 'Introduction to Computer Science',
            'cohort': 'Fall 2024',
            'section': 'Section A',
            'instructors': ['Dr. Ahmed Khan', 'Dr. Fatima Ali'],
            'semester': 'Fall',
            'year': 2024,
            'status': 'Active',
            'student_count': 22,
            'assessment_count': 3,
            'clos_covered': 5,
        },
        {
            'id': 2,
            'course_code': 'CS-201',
            'course_name': 'Data Structures and Algorithms',
            'cohort': 'Fall 2024',
            'section': 'Section A',
            'instructors': ['Dr. Muhammad Usman'],
            'semester': 'Fall',
            'year': 2024,
            'status': 'Active',
            'student_count': 23,
            'assessment_count': 4,
            'clos_covered': 4,
        },
        {
            'id': 3,
            'course_code': 'CS-202',
            'course_name': 'Database Management Systems',
            'cohort': 'Spring 2025',
            'section': 'Section A',
            'instructors': ['Dr. Ayesha Siddiqui'],
            'semester': 'Spring',
            'year': 2025,
            'status': 'Pending',
            'student_count': 0,
            'assessment_count': 0,
            'clos_covered': 0,
        },
        {
            'id': 4,
            'course_code': 'CS-302',
            'course_name': 'Software Engineering',
            'cohort': 'Fall 2024',
            'section': 'Section B',
            'instructors': ['Dr. Bilal Ahmed'],
            'semester': 'Fall',
            'year': 2024,
            'status': 'Completed',
            'student_count': 21,
            'assessment_count': 5,
            'clos_covered': 6,
        },
        {
            'id': 5,
            'course_code': 'CS-301',
            'course_name': 'Operating Systems',
            'cohort': 'Spring 2025',
            'section': 'Section A',
            'instructors': ['Dr. Ahmed Khan'],
            'semester': 'Spring',
            'year': 2025,
            'status': 'Pending',
            'student_count': 0,
            'assessment_count': 0,
            'clos_covered': 0,
        },
    ]
    return render(request, 'offering_list.html', {'offerings': offerings})

def offering_create(request):
    # Dummy data for dropdowns (simulating data from Module 2 & 3)
    courses = [
        {'id': 1, 'code': 'CS-101', 'name': 'Introduction to Computer Science', 'credits': 3},
        {'id': 2, 'code': 'CS-102', 'name': 'Programming Fundamentals', 'credits': 4},
        {'id': 3, 'code': 'CS-201', 'name': 'Data Structures and Algorithms', 'credits': 4},
        {'id': 4, 'code': 'CS-202', 'name': 'Database Management Systems', 'credits': 3},
        {'id': 5, 'code': 'CS-301', 'name': 'Operating Systems', 'credits': 3},
        {'id': 6, 'code': 'CS-302', 'name': 'Software Engineering', 'credits': 3},
        {'id': 7, 'code': 'CS-401', 'name': 'Artificial Intelligence', 'credits': 3},
        {'id': 8, 'code': 'MATH-101', 'name': 'Calculus I', 'credits': 3},
        {'id': 9, 'code': 'PHY-101', 'name': 'Physics I', 'credits': 4},
        {'id': 10, 'code': 'ENG-101', 'name': 'English Composition', 'credits': 3},
    ]
    
    # Cohorts from Module 3
    cohorts = [
        {'id': 1, 'name': 'Fall 2024', 'program_code': 'BSCS'},
        {'id': 2, 'name': 'Spring 2025', 'program_code': 'BSEE'},
        {'id': 3, 'name': 'Fall 2023', 'program_code': 'BSME'},
        {'id': 4, 'name': 'Spring 2024', 'program_code': 'BBA'},
        {'id': 5, 'name': 'Fall 2025', 'program_code': 'BSCS'},
    ]
    
    # Sections from Module 3
    sections = [
        {'id': 1, 'name': 'Section A', 'cohort_id': 1},
        {'id': 2, 'name': 'Section B', 'cohort_id': 1},
        {'id': 3, 'name': 'Section A', 'cohort_id': 2},
        {'id': 4, 'name': 'Section A', 'cohort_id': 3},
        {'id': 5, 'name': 'Section B', 'cohort_id': 3},
        {'id': 6, 'name': 'Section A', 'cohort_id': 4},
        {'id': 7, 'name': 'Section A', 'cohort_id': 5},
    ]
    
    # Instructors from Module 1
    instructors = [
        {'id': 1, 'name': 'Dr. Ahmed Khan'},
        {'id': 2, 'name': 'Dr. Fatima Ali'},
        {'id': 3, 'name': 'Dr. Muhammad Usman'},
        {'id': 4, 'name': 'Dr. Ayesha Siddiqui'},
        {'id': 5, 'name': 'Dr. Bilal Ahmed'},
        {'id': 6, 'name': 'Dr. Sarah Mahmood'},
    ]
    
    context = {
        'is_edit': False,
        'offering': None,
        'courses': courses,
        'cohorts': cohorts,
        'sections': sections,
        'instructors': instructors,
        'semesters': ['Fall', 'Spring', 'Summer'],
        'years': range(2020, 2027),
    }
    return render(request, 'offering_form.html', context)

def offering_edit(request, pk):
    # Dummy data for editing
    courses = [
        {'id': 1, 'code': 'CS-101', 'name': 'Introduction to Computer Science', 'credits': 3},
        {'id': 2, 'code': 'CS-102', 'name': 'Programming Fundamentals', 'credits': 4},
        {'id': 3, 'code': 'CS-201', 'name': 'Data Structures and Algorithms', 'credits': 4},
        {'id': 4, 'code': 'CS-202', 'name': 'Database Management Systems', 'credits': 3},
    ]
    
    cohorts = [
        {'id': 1, 'name': 'Fall 2024', 'program_code': 'BSCS'},
        {'id': 2, 'name': 'Spring 2025', 'program_code': 'BSEE'},
    ]
    
    sections = [
        {'id': 1, 'name': 'Section A', 'cohort_id': 1},
        {'id': 2, 'name': 'Section B', 'cohort_id': 1},
        {'id': 3, 'name': 'Section A', 'cohort_id': 2},
    ]
    
    instructors = [
        {'id': 1, 'name': 'Dr. Ahmed Khan'},
        {'id': 2, 'name': 'Dr. Fatima Ali'},
        {'id': 3, 'name': 'Dr. Muhammad Usman'},
        {'id': 4, 'name': 'Dr. Ayesha Siddiqui'},
    ]
    
    # Dummy existing offering data
    offering = {
        'id': pk,
        'course_id': 1,
        'cohort_id': 1,
        'section_id': 1,
        'instructor_ids': [1, 2],
        'semester': 'Fall',
        'year': 2024,
        'status': 'Active',
    }
    
    context = {
        'is_edit': True,
        'offering': offering,
        'courses': courses,
        'cohorts': cohorts,
        'sections': sections,
        'instructors': instructors,
        'semesters': ['Fall', 'Spring', 'Summer'],
        'years': range(2020, 2027),
    }
    return render(request, 'offering_form.html', context)

def offering_detail(request, pk):
    # Dummy data for a specific offering
    offering = {
        'id': pk,
        'course_code': 'CS-101',
        'course_name': 'Introduction to Computer Science',
        'course_credits': 3,
        'cohort': 'Fall 2024',
        'section': 'Section A',
        'instructors': ['Dr. Ahmed Khan', 'Dr. Fatima Ali'],
        'semester': 'Fall',
        'year': 2024,
        'status': 'Active',
        'student_count': 22,
        'assessment_count': 3,
        'clos_covered': 5,
        'students': [
            {'id': 1, 'name': 'Ahmed Khan', 'student_id': '2024-001', 'email': 'ahmed.k@email.com'},
            {'id': 2, 'name': 'Fatima Ali', 'student_id': '2024-002', 'email': 'fatima.a@email.com'},
            {'id': 3, 'name': 'Muhammad Usman', 'student_id': '2024-003', 'email': 'm.usman@email.com'},
            {'id': 4, 'name': 'Ayesha Siddiqui', 'student_id': '2024-004', 'email': 'ayesha.s@email.com'},
            {'id': 5, 'name': 'Bilal Ahmed', 'student_id': '2024-005', 'email': 'bilal.a@email.com'},
            {'id': 6, 'name': 'Hira Malik', 'student_id': '2024-006', 'email': 'hira.m@email.com'},
            {'id': 7, 'name': 'Omar Farooq', 'student_id': '2024-007', 'email': 'omar.f@email.com'},
            {'id': 8, 'name': 'Zara Abbas', 'student_id': '2024-008', 'email': 'zara.a@email.com'},
        ],
        'assessments': [
            {'id': 1, 'name': 'Quiz 1', 'tool': 'Quiz', 'max_marks': 10, 'weightage': 10, 'clos': ['CLO-1', 'CLO-2']},
            {'id': 2, 'name': 'Midterm', 'tool': 'Midterm', 'max_marks': 30, 'weightage': 30, 'clos': ['CLO-1', 'CLO-2', 'CLO-3']},
            {'id': 3, 'name': 'Final Project', 'tool': 'Final Project', 'max_marks': 20, 'weightage': 20, 'clos': ['CLO-3', 'CLO-4']},
        ],
        'clos': [
            {'id': 1, 'code': 'CLO-1', 'description': 'Apply basic programming concepts'},
            {'id': 2, 'code': 'CLO-2', 'description': 'Design simple algorithms'},
            {'id': 3, 'code': 'CLO-3', 'description': 'Implement data structures'},
            {'id': 4, 'code': 'CLO-4', 'description': 'Analyze algorithm efficiency'},
            {'id': 5, 'code': 'CLO-5', 'description': 'Create software solutions'},
        ],
    }
    return render(request, 'offering_detail.html', {'offering': offering})


# ==================== INSTRUCTOR DASHBOARD VIEW ====================

def instructor_dashboard(request):
    # Dummy instructor data (replace with actual user data later)
    instructor = {
        'name': 'Dr. Ahmed Khan',
        'email': 'ahmed.khan@university.edu',
        'department': 'Computer Science',
        'total_courses': 3,
        'total_students': 66,
        'pending_tasks': 2,
        'reports': 5,
    }
    
    # Dummy courses assigned to this instructor
    courses = [
        {
            'id': 10,
            'code': 'CS-101',
            'name': 'Introduction to Computer Science',
            'semester': 'Fall 2024',
            'section': 'Section A',
            'student_count': 22,
            'status': 'Active',
            'progress': 78,
            'assessments': 3,
            'clos': 5,
        },
        {
            'id': 20,
            'code': 'CS-201',
            'name': 'Data Structures and Algorithms',
            'semester': 'Fall 2024',
            'section': 'Section A',
            'student_count': 23,
            'status': 'Active',
            'progress': 82,
            'assessments': 4,
            'clos': 4,
        },
        {
            'id': 4,
            'code': 'CS-302',
            'name': 'Software Engineering',
            'semester': 'Spring 2025',
            'section': 'Section B',
            'student_count': 21,
            'status': 'Pending',
            'progress': 0,
            'assessments': 0,
            'clos': 6,
        },
    ]
    
    context = {
        'instructor': instructor,
        'courses': courses,
    }
    return render(request, 'instructor_dashboard.html', context)



# ==================== SURVEY VIEWS ====================

def survey_list(request):
    surveys = [
        {
            'id': 10,
            'title': 'Course Feedback - CS-101',
            'description': 'Collect feedback from students about course content, delivery, and learning experience.',
            'type': 'Student Feedback',
            'status': 'active',         
            'responses': 22,
            'target_responses': 32,
            'due_date': '2024-12-20',
            'days_left': 5,
            'response_rate': 68,
            'created_at': '2024-11-01',
        },
        {
            'id': 2,
            'title': 'CS-201 Teaching Evaluation',
            'description': 'Evaluate teaching effectiveness, clarity, and student engagement in Data Structures.',
            'type': 'Course Evaluation',
            'status': 'active',
            'responses': 18,
            'target_responses': 35,
            'due_date': '2024-12-25',
            'days_left': 10,
            'response_rate': 52,
            'created_at': '2024-11-15',
        },
        {
            'id': 55,
            'title': 'Program Outcomes Survey',
            'description': 'Survey to evaluate program outcomes and learning objectives for accreditation.',
            'type': 'Program Survey',
            'status': 'draft',
            'responses': 0,
            'target_responses': 0,
            'due_date': None,
            'days_left': None,           
            'response_rate': 0,
            'created_at': '2024-12-01',
        },
        {
            'id': 4,
            'title': 'CS-302 Course Feedback',
            'description': 'End-of-semester feedback for Software Engineering course.',
            'type': 'Course Evaluation',
            'status': 'closed',
            'responses': 21,
            'target_responses': 24,
            'due_date': '2024-12-10',
            'days_left': None,            
            'response_rate': 88,
            'created_at': '2024-10-01',
        },
        {
            'id': 5,
            'title': 'Instructor Evaluation Survey',
            'description': 'Anonymous feedback on instructor performance and teaching methods.',
            'type': 'Instructor Feedback',
            'status': 'active',
            'responses': 35,
            'target_responses': 50,
            'due_date': '2025-01-15',
            'days_left': 28,
            'response_rate': 71,
            'created_at': '2024-11-20',
        },
    ]

    # Compute summary stats so the template doesn't hardcode them
    total_surveys    = len(surveys)
    active_surveys   = sum(1 for s in surveys if s['status'] == 'active')
    total_responses  = sum(s['responses'] for s in surveys)
    rated_surveys    = [s for s in surveys if s['response_rate'] > 0]
    avg_response_rate = (
        round(sum(s['response_rate'] for s in rated_surveys) / len(rated_surveys))
        if rated_surveys else 0
    )

    context = {
        'surveys': surveys,
        'total_surveys': total_surveys,
        'active_surveys': active_surveys,
        'total_responses': total_responses,
        'avg_response_rate': avg_response_rate,
    }
    return render(request, 'survey_list.html', context)

def survey_builder(request, offering_id):
    # Get course details from offering (dummy data)
    offering = {
        'id': offering_id,
        'course_code': 'CS-101',
        'course_name': 'Introduction to Computer Science',
        'section': 'Section A',
        'student_count': 22,
    }
    context = {
        'offering': offering,
    }
    return render(request, 'survey_builder.html', context)

def survey_results(request, pk):
    # Dummy data for survey results
    survey = {
        'id': pk,
        'title': 'Mid-Semester Survey Results',
        'course': 'CS-101 - Introduction to Computer Science',
        'semester': 'Fall 2024',
        'section': 'Section A',
        'total_responses': 15,
        'total_students': 22,
        'response_rate': 68,
        'average_score': 4.2,
        'sentiment': 'Positive',
        'avg_completion_time': '6m',
    }
    return render(request, 'survey_results.html', {'survey': survey})


DEMO_CONTROLLERS = [
    {'id': 1, 'name': 'Dr. Farhan Ahmed', 'email': 'farhan.ahmed@university.edu', 'department': 'Computer Science', 'active_programs': 1},
    {'id': 2, 'name': 'Dr. Nusrat Jahan', 'email': 'nusrat.jahan@university.edu', 'department': 'Electrical & Electronic Engineering', 'active_programs': 1},
    {'id': 3, 'name': 'Dr. Imran Kabir', 'email': 'imran.kabir@university.edu', 'department': 'Civil Engineering', 'active_programs': 1},
    {'id': 4, 'name': 'Dr. Sabrina Islam', 'email': 'sabrina.islam@university.edu', 'department': 'Business Administration', 'active_programs': 1},
    {'id': 5, 'name': 'Dr. Tanvir Hasan', 'email': 'tanvir.hasan@university.edu', 'department': 'Mechanical Engineering', 'active_programs': 0},
    {'id': 6, 'name': 'Dr. Mahmuda Khatun', 'email': 'mahmuda.khatun@university.edu', 'department': 'Information Technology', 'active_programs': 0},
]

DEMO_PROGRAMS = [
    {'id': 1, 'code': 'BSCS', 'name': 'Bachelor of Science in Computer Science', 'version': 3, 'status': 'Active', 'peo_count': 3, 'plo_count': 6, 'controller_id': 1, 'created_on': 'Mar 20, 2025', 'last_updated': 'May 14, 2026'},
    {'id': 2, 'code': 'BSEEE', 'name': 'Bachelor of Science in Electrical & Electronic Engineering', 'version': 1, 'status': 'Active', 'peo_count': 3, 'plo_count': 5, 'controller_id': 2, 'created_on': 'Jan 18, 2026', 'last_updated': 'Jan 18, 2026'},
    {'id': 3, 'code': 'BSCE', 'name': 'Bachelor of Science in Civil Engineering', 'version': 1, 'status': 'Draft', 'peo_count': 2, 'plo_count': 8, 'controller_id': 3, 'created_on': 'Feb 02, 2026', 'last_updated': 'Feb 02, 2026'},
    {'id': 4, 'code': 'BBA', 'name': 'Bachelor of Business Administration', 'version': 2, 'status': 'Archived', 'peo_count': 4, 'plo_count': 11, 'controller_id': 4, 'created_on': 'Sep 10, 2024', 'last_updated': 'Nov 02, 2025'},
    {'id': 5, 'code': 'BSME', 'name': 'Bachelor of Science in Mechanical Engineering', 'version': 0, 'status': 'New', 'peo_count': 0, 'plo_count': 0, 'controller_id': 5, 'created_on': 'Jun 01, 2026', 'last_updated': 'Jun 01, 2026'},
    {'id': 6, 'code': 'BSIT', 'name': 'Bachelor of Science in Information Technology', 'version': 0, 'status': 'New', 'peo_count': 0, 'plo_count': 0, 'controller_id': 6, 'created_on': 'Jun 15, 2026', 'last_updated': 'Jun 15, 2026'},
]


def get_controller(controller_id):
    return next((c for c in DEMO_CONTROLLERS if c['id'] == controller_id), None)


def _with_mapping_rows(snapshot):
    snapshot = dict(snapshot)
    peos = snapshot.get('peos', [])
    plos = snapshot.get('plos', [])
    mapping = snapshot.get('mapping', [])

    rows = []
    for plo_idx, plo in enumerate(plos):
        cells = []
        for peo_idx in range(len(peos)):
            row = mapping[peo_idx] if peo_idx < len(mapping) else []
            cells.append(bool(row[plo_idx]) if plo_idx < len(row) else False)
        rows.append({'plo_title': plo.get('title', ''), 'cells': cells})

    snapshot['mapping_rows'] = rows
    return snapshot



DEMO_PROGRAM_VERSIONS = {
    1: [  # BSCS — 3 versions
        {
            'version': 1,
            'date': 'Mar 20, 2025',
            'editor': 'Dr. Farhan Ahmed',
            'sections_changed': ['Mission & Vision', 'PEOs', 'PLOs', 'PEO-PLO Mapping', 'Settings & Assessment Tools'],
            'comments': {
                'Mission & Vision': 'Initial setup based on department curriculum committee draft.',
                'PEOs': 'Initial PEOs adapted from outgoing curriculum.',
                'PLOs': 'Imported ABET preset and adjusted wording for local context.',
                'PEO-PLO Mapping': 'Initial mapping drafted with curriculum committee.',
                'Settings & Assessment Tools': 'Initial assessment tools selected.',
            },
            'snapshot': {
                'inst_vision': 'To be a globally recognized institution advancing knowledge and innovation for the betterment of society.',
                'inst_missions': ['To advance knowledge through excellence in teaching and research.'],
                'program_vision': 'To be a leading program producing computer science graduates equipped for industry.',
                'program_missions': [
                    'To provide a solid computing curriculum.',
                    'To prepare graduates for the software industry.',
                ],
                'peos': [
                    {'title': 'Professionalism', 'description': 'Graduates will practice with integrity and professionalism.'},
                    {'title': 'Technical Competence', 'description': 'Graduates will apply core computing principles to solve problems.'},
                    {'title': 'Lifelong Learning', 'description': 'Graduates will pursue continued learning.'},
                ],
                'plos': [
                    {'title': 'Engineering knowledge', 'description': 'Apply knowledge of computing and mathematics to solve problems.'},
                    {'title': 'Problem analysis', 'description': 'Identify and analyze computing problems.'},
                    {'title': 'Design/development of solutions', 'description': 'Design software solutions for specified needs.'},
                    {'title': 'Tool usage', 'description': 'Use standard computing tools and techniques.'},
                    {'title': 'Communication', 'description': 'Communicate technical work effectively.'},
                ],
                'mapping': [
                    [True, True, False, False, True],
                    [True, True, True, True, False],
                    [False, False, True, True, True],
                ],
                'assessment_tools': ['Quiz', 'Midterm', 'Final Project'],
                'assessment_tools_custom': [],
            },
        },
        {
            'version': 2,
            'date': 'Nov 02, 2025',
            'editor': 'Dr. Farhan Ahmed',
            'sections_changed': ['Mission & Vision', 'Settings & Assessment Tools'],
            'comments': {
                'Mission & Vision': 'Revised program mission to reflect new research focus areas.',
                'Settings & Assessment Tools': 'Added Capstone Defense as a recurring assessment tool.',
            },
            'snapshot': {
                'inst_vision': 'To be a globally recognized institution advancing knowledge and innovation for the betterment of society.',
                'inst_missions': [
                    'To advance knowledge through excellence in teaching and research.',
                    'To cultivate ethical, socially responsible leaders.',
                ],
                'program_vision': 'To be a leading program producing computer science graduates who innovate and lead in a digital world.',
                'program_missions': [
                    'To provide a rigorous, industry-relevant computing curriculum.',
                    'To foster research and innovation in emerging technologies.',
                ],
                'peos': [
                    {'title': 'Professionalism', 'description': 'Graduates will practice with integrity and professionalism.'},
                    {'title': 'Technical Competence', 'description': 'Graduates will apply core computing principles to solve problems.'},
                    {'title': 'Lifelong Learning', 'description': 'Graduates will pursue continued learning.'},
                ],
                'plos': [
                    {'title': 'Engineering knowledge', 'description': 'Apply knowledge of computing and mathematics to solve problems.'},
                    {'title': 'Problem analysis', 'description': 'Identify and analyze computing problems.'},
                    {'title': 'Design/development of solutions', 'description': 'Design software solutions for specified needs.'},
                    {'title': 'Tool usage', 'description': 'Use standard computing tools and techniques.'},
                    {'title': 'Communication', 'description': 'Communicate technical work effectively.'},
                ],
                'mapping': [
                    [True, True, False, False, True],
                    [True, True, True, True, False],
                    [False, False, True, True, True],
                ],
                'assessment_tools': ['Quiz', 'Midterm', 'Final Project', 'Presentation'],
                'assessment_tools_custom': ['Capstone Defense'],
            },
        },
        {
            'version': 3,
            'date': 'May 14, 2026',
            'editor': 'Dr. Farhan Ahmed',
            'sections_changed': ['PLOs', 'PEO-PLO Mapping'],
            'comments': {
                'PLOs': 'Updated wording on Tool Usage to match latest ABET descriptor and added Ethics PLO.',
                'PEO-PLO Mapping': 'Re-mapped after PLO wording update and new Ethics PLO.',
            },
            'snapshot': {
                'inst_vision': 'To be a globally recognized institution advancing knowledge and innovation for the betterment of society.',
                'inst_missions': [
                    'To advance knowledge through excellence in teaching and research.',
                    'To cultivate ethical, socially responsible leaders.',
                ],
                'program_vision': 'To be a leading program producing computer science graduates who innovate and lead in a digital world.',
                'program_missions': [
                    'To provide a rigorous, industry-relevant computing curriculum.',
                    'To foster research and innovation in emerging technologies.',
                    'To instill professional and ethical responsibility in graduates.',
                ],
                'peos': [
                    {'title': 'Professionalism', 'description': 'Graduates will engage in professional practice with integrity, ethics, and respect for diversity.'},
                    {'title': 'Technical Excellence', 'description': 'Graduates will apply advanced computing principles to design and develop robust, scalable software solutions.'},
                    {'title': 'Lifelong Learning', 'description': 'Graduates will pursue continued learning and professional development throughout their careers.'},
                ],
                'plos': [
                    {'title': 'Engineering knowledge', 'description': 'Apply knowledge of computing, mathematics, and science to solve complex computing problems.'},
                    {'title': 'Problem analysis', 'description': 'Identify, formulate, and analyze complex computing problems using first principles.'},
                    {'title': 'Design/development of solutions', 'description': 'Design solutions for complex computing problems and design software systems that meet specified needs.'},
                    {'title': 'Modern tool usage', 'description': 'Create, select, and apply appropriate techniques, resources, and modern computing tools.'},
                    {'title': 'Communication', 'description': 'Communicate effectively on complex computing activities with the community and society at large.'},
                    {'title': 'Ethics', 'description': 'Apply ethical principles and commit to professional ethics and responsibilities of computing practice.'},
                ],
                'mapping': [
                    [True, True, False, False, True, True],
                    [True, True, True, True, False, False],
                    [False, False, True, True, True, False],
                ],
                'assessment_tools': ['Quiz', 'Midterm', 'Final Project', 'Presentation'],
                'assessment_tools_custom': ['Capstone Defense'],
            },
        },
    ],
    2: [  # BSEEE — 1 version
        {
            'version': 1,
            'date': 'Jan 18, 2026',
            'editor': 'Dr. Nusrat Jahan',
            'sections_changed': ['Mission & Vision', 'PEOs', 'PLOs', 'PEO-PLO Mapping', 'Settings & Assessment Tools'],
            'comments': {
                'Mission & Vision': 'Initial program setup.',
                'PEOs': 'Initial PEOs drafted with department input.',
                'PLOs': 'Imported BAETE preset.',
                'PEO-PLO Mapping': 'Initial mapping drafted.',
                'Settings & Assessment Tools': 'Initial assessment tools selected.',
            },
            'snapshot': {
                'inst_vision': 'To be a globally recognized institution advancing knowledge and innovation for the betterment of society.',
                'inst_missions': ['To advance knowledge through excellence in teaching and research.'],
                'program_vision': 'To be a recognized leader in electrical and electronic engineering education and innovation.',
                'program_missions': [
                    'To deliver a strong foundation in electrical and electronic engineering principles.',
                    'To prepare graduates for industry, research, and entrepreneurship.',
                ],
                'peos': [
                    {'title': 'Technical Competence', 'description': 'Graduates will apply electrical and electronic engineering principles to solve real-world problems.'},
                    {'title': 'Professional Growth', 'description': 'Graduates will pursue continued professional development and leadership roles.'},
                    {'title': 'Societal Impact', 'description': 'Graduates will contribute engineering solutions that benefit society and the environment.'},
                ],
                'plos': [
                    {'title': 'Engineering knowledge', 'description': 'Apply knowledge of mathematics, science, and engineering fundamentals to electrical and electronic systems.'},
                    {'title': 'Design/development of solutions', 'description': 'Design electrical and electronic systems that meet specified needs.'},
                    {'title': 'Modern tool usage', 'description': 'Apply modern engineering and IT tools to electrical engineering activities.'},
                    {'title': 'Ethics', 'description': 'Apply ethical principles in engineering practice.'},
                    {'title': 'Communication', 'description': 'Communicate effectively with technical and non-technical audiences.'},
                ],
                'mapping': [
                    [True, True, True, False, False],
                    [False, True, True, True, False],
                    [True, False, False, True, True],
                ],
                'assessment_tools': ['Quiz', 'Midterm', 'Lab Report', 'Practical Exam'],
                'assessment_tools_custom': [],
            },
        },
    ],
}


def _section_complete(program_id):
    """Has this program been configured at least once (version >= 1)?"""
    program = next((p for p in DEMO_PROGRAMS if p['id'] == program_id), None)
    return bool(program and program['version'] > 0)


def dean_dashboard(request):
    
    total_programs = len(DEMO_PROGRAMS)
    active_programs = len([p for p in DEMO_PROGRAMS if p['status'] == 'Active'])
    pending_programs = [p for p in DEMO_PROGRAMS if p['version'] == 0]
    total_controllers = len(DEMO_CONTROLLERS)
    unassigned_controllers = len([c for c in DEMO_CONTROLLERS if c['active_programs'] == 0])

    recent_activity = [
        {'icon': 'fa-code-branch', 'color': 'indigo', 'text': 'BSCS was updated to v3 by Dr. Farhan Ahmed.', 'time': '1 month ago'},
        {'icon': 'fa-user-plus', 'color': 'emerald', 'text': 'Assigned Dr. Mahmuda Khatun as controller for BSIT.', 'time': '1 week ago'},
        {'icon': 'fa-plus-circle', 'color': 'sky', 'text': 'Created new program: BSIT.', 'time': '1 week ago'},
        {'icon': 'fa-code-branch', 'color': 'indigo', 'text': 'BSCE was configured for the first time (v1) by Dr. Imran Kabir.', 'time': '4 months ago'},
    ]

    context = {
        'today': date.today().strftime('%A, %B %d, %Y'),
        'stats': {
            'total_programs': total_programs,
            'active_programs': active_programs,
            'pending_programs': len(pending_programs),
            'total_controllers': total_controllers,
            'unassigned_controllers': unassigned_controllers,
        },
        'pending_program_list': pending_programs,
        'recent_activity': recent_activity,
    }
    return render(request, 'dean_dashboard.html', context)


def dean_program_list(request):
    programs = []
    for p in DEMO_PROGRAMS:
        controller = get_controller(p['controller_id'])
        programs.append({**p, 'controller': controller})

    context = {'programs': programs}
    return render(request, 'dean_program_list.html', context)


def dean_program_create(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        name = request.POST.get('name', '').strip()
        controller_id = request.POST.get('controller_id', '')

        errors = {}
        if not code:
            errors['code'] = 'Program code is required.'
        if not name:
            errors['name'] = 'Program name is required.'
        if not controller_id:
            errors['controller_id'] = 'Please assign a program controller.'

        if not errors:
            new_id = max(p['id'] for p in DEMO_PROGRAMS) + 1
            DEMO_PROGRAMS.append({
                'id': new_id,
                'code': code,
                'name': name,
                'version': 0,
                'status': 'New',
                'peo_count': 0,
                'plo_count': 0,
                'controller_id': int(controller_id),
                'created_on': date.today().strftime('%b %d, %Y'),
                'last_updated': date.today().strftime('%b %d, %Y'),
            })
            return redirect('dean_program_list')

        context = {
            'controllers': DEMO_CONTROLLERS,
            'errors': errors,
            'form_data': {'code': code, 'name': name, 'controller_id': controller_id},
        }
        return render(request, 'dean_program_create.html', context)

    context = {'controllers': DEMO_CONTROLLERS, 'errors': {}, 'form_data': {}}
    return render(request, 'dean_program_create.html', context)


def dean_program_detail(request, program_id):
    program = next((p for p in DEMO_PROGRAMS if p['id'] == program_id), None)
    if program is None:
        return render(request, 'dean_program_list.html', {
            'programs': DEMO_PROGRAMS,
            'error': 'Program not found.',
        })

    controller = get_controller(program['controller_id'])
    versions = DEMO_PROGRAM_VERSIONS.get(program_id, [])
    # Current state = snapshot of the latest version (or empty shell if never configured)
    current_snapshot_raw = versions[-1]['snapshot'] if versions else {
        'inst_vision': '', 'inst_missions': [], 'program_vision': '', 'program_missions': [],
        'peos': [], 'plos': [], 'mapping': [], 'assessment_tools': [], 'assessment_tools_custom': [],
    }
    current_snapshot = _with_mapping_rows(current_snapshot_raw)

    versions_desc = []
    for v in reversed(versions):
        v = dict(v)
        v['snapshot'] = _with_mapping_rows(v['snapshot'])
        versions_desc.append(v)

    context = {
        'program': program,
        'controller': controller,
        'current_snapshot': current_snapshot,
        'versions': versions_desc,
        'is_unconfigured': program['version'] == 0,
    }
    return render(request, 'dean_program_detail.html', context)
