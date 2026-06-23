from django.urls import path
from . import views

urlpatterns = [
    # The main dashboard (will just extend base.html for now)
    path('', views.dashboard, name='dashboard'),
    path('programs/', views.program_list, name='program_list'),
    path('programs/create/', views.program_create, name='program_create'),
    path('programs/<int:program_id>/edit/', views.program_edit, name='program_edit'),
    path('programs/<int:program_id>/update/', views.program_update, name='program_update'),
    path('programs/<int:program_id>/edit/', views.program_edit, name='program_edit'),
    path('programs/plo-presets/<str:source>/', views.plo_preset_import, name='plo_preset_import'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('programs/<int:pk>/mapping/', views.program_mapping, name='program_mapping'),
    path('cohorts/', views.cohort_list, name='cohort_list'),
    path('cohorts/create/', views.cohort_create, name='cohort_create'),
    path('cohorts/<int:pk>/edit/', views.cohort_edit, name='cohort_edit'),
    path('cohorts/<int:pk>/', views.cohort_detail, name='cohort_detail'),
    path('cohorts/<int:pk>/upload/', views.cohort_upload, name='cohort_upload'),
    path('cohorts/<int:pk>/sections/', views.cohort_sections, name='cohort_sections'),
    path('offerings/', views.offering_list, name='offering_list'),
    path('offerings/create/', views.offering_create, name='offering_create'),
    path('offerings/<int:pk>/edit/', views.offering_edit, name='offering_edit'),

    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('offerings/<int:pk>/', views.offering_detail, name='offering_detail'),

    path('surveys/', views.survey_list, name='survey_list'),
    path('surveys/builder/<int:offering_id>/', views.survey_builder, name='survey_builder'),
    path('surveys/<int:pk>/results/', views.survey_results, name='survey_results'),

    path('dean/dashboard/', views.dean_dashboard, name='dean_dashboard'),
    path('dean/programs/', views.dean_program_list, name='dean_program_list'),
    path('dean/programs/create/', views.dean_program_create, name='dean_program_create'),
    path('dean/programs/<int:program_id>/', views.dean_program_detail, name='dean_program_detail'),
    
]
