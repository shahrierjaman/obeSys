from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# ============================================================================
# USER & ROLES (Extended User model)
# ============================================================================

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('dean', 'Dean'),
        ('program_controller', 'Program Controller'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"


# ============================================================================
# PROGRAM MANAGEMENT
# ============================================================================

class Program(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    program_controller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_programs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    current_version = models.IntegerField(default=0)
    vision = models.TextField(blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def increment_version(self):
        self.current_version += 1
        return self.current_version


class ProgramVersion(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='program_versions_created')
    created_at = models.DateTimeField(auto_now_add=True)
    sections_modified = models.JSONField(default=list)  # List of modified sections
    comments = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('program', 'version_number')
        ordering = ['-version_number']
    
    def __str__(self):
        return f"{self.program.code} - v{self.version_number}"


class ChangeLog(models.Model):
    program_version = models.ForeignKey(ProgramVersion, on_delete=models.CASCADE, related_name='changes')
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Change to {self.field_name} in {self.program_version}"


# ============================================================================
# PROGRAM EDUCATIONAL OBJECTIVES (PEOs)
# ============================================================================

class ProgramEducationalObjective(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='peos')
    code = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order_index', 'id']
    
    def __str__(self):
        return f"PEO: {self.title} ({self.program.code})"


# ============================================================================
# PROGRAM LEARNING OUTCOMES (PLOs)
# ============================================================================

class ProgramLearningOutcome(models.Model):
    SOURCE_CHOICES = [
        ('custom', 'Custom'),
        ('abet', 'ABET'),
        ('baete', 'BAETE'),
        ('ieee', 'IEEE'),
    ]
    
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='plos')
    code = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order_index = models.IntegerField(default=0)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='custom')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order_index', 'id']
    
    def __str__(self):
        return f"PLO: {self.title} ({self.program.code})"


# ============================================================================
# PEO-PLO MAPPING
# ============================================================================

class PEOPLOMapping(models.Model):
    STRENGTH_CHOICES = [
        ('weak', 'Weak'),
        ('medium', 'Medium'),
        ('strong', 'Strong'),
    ]
    
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='peo_plo_mappings')
    peo = models.ForeignKey(ProgramEducationalObjective, on_delete=models.CASCADE, related_name='plo_mappings')
    plo = models.ForeignKey(ProgramLearningOutcome, on_delete=models.CASCADE, related_name='peo_mappings')
    strength = models.CharField(max_length=20, choices=STRENGTH_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('peo', 'plo')
    
    def __str__(self):
        return f"{self.peo.title} → {self.plo.title} ({self.strength})"


# ============================================================================
# COURSES
# ============================================================================

class Course(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    credit_hours = models.DecimalField(max_digits=3, decimal_places=1)
    semester_offered = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class CourseProgramMapping(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='program_mappings')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='course_mappings')
    is_required = models.BooleanField(default=True)
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'program')
    
    def __str__(self):
        return f"{self.course.code} → {self.program.code}"


# ============================================================================
# COURSE LEARNING OUTCOMES (CLOs)
# ============================================================================

class CourseLearningOutcome(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='clos')
    code = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order_index', 'id']
    
    def __str__(self):
        return f"CLO: {self.title} ({self.course.code})"


# ============================================================================
# CLO-PLO MAPPING
# ============================================================================

class CLOPLOMapping(models.Model):
    STRENGTH_CHOICES = [
        ('weak', 'Weak'),
        ('medium', 'Medium'),
        ('strong', 'Strong'),
    ]
    
    clo = models.ForeignKey(CourseLearningOutcome, on_delete=models.CASCADE, related_name='plo_mappings')
    plo = models.ForeignKey(ProgramLearningOutcome, on_delete=models.CASCADE, related_name='clo_mappings')
    strength = models.CharField(max_length=20, choices=STRENGTH_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('clo', 'plo')
    
    def __str__(self):
        return f"{self.clo.title} → {self.plo.title} ({self.strength})"


# ============================================================================
# COHORTS & SECTIONS
# ============================================================================

class Cohort(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    program = models.ForeignKey(Program, on_delete=models.PROTECT, related_name='cohorts')
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255)
    start_year = models.IntegerField(blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    total_students = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.program.code} - {self.name}"


class CohortSection(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='sections')
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255)
    total_students = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"{self.cohort.name} - {self.name}"


# ============================================================================
# STUDENTS
# ============================================================================

class Student(models.Model):
    ENROLLMENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
        ('transferred', 'Transferred'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=50, unique=True)
    cohort = models.ForeignKey(Cohort, on_delete=models.PROTECT, related_name='students')
    section = models.ForeignKey(CohortSection, on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['student_id']
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"


# ============================================================================
# COURSE OFFERINGS
# ============================================================================

class CourseOffering(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='offerings')
    cohort = models.ForeignKey(Cohort, on_delete=models.PROTECT, related_name='course_offerings')
    section = models.ForeignKey(CohortSection, on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='taught_offerings')
    semester = models.CharField(max_length=20, blank=True, null=True)  # e.g., "Fall 2024"
    year = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    enrolled_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-semester']
    
    def __str__(self):
        return f"{self.course.code} - {self.cohort.name} ({self.semester})"


class StudentEnrollment(models.Model):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='student_enrollments')
    grade = models.CharField(max_length=2, blank=True, null=True)
    gpa_points = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    enrollment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('student', 'course_offering')
    
    def __str__(self):
        return f"{self.student.student_id} → {self.course_offering.course.code}"


# ============================================================================
# ASSESSMENTS
# ============================================================================

class AssessmentTool(models.Model):
    TOOL_TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('custom', 'Custom'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    tool_type = models.CharField(max_length=20, choices=TOOL_TYPE_CHOICES, default='standard')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Assessment(models.Model):
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='assessments')
    tool = models.ForeignKey(AssessmentTool, on_delete=models.SET_NULL, null=True, related_name='assessments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    max_marks = models.IntegerField(validators=[MinValueValidator(1)])
    weightage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    due_date = models.DateField(blank=True, null=True)
    assessment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.course_offering.course.code})"


class AssessmentCLOMapping(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='clo_mappings')
    clo = models.ForeignKey(CourseLearningOutcome, on_delete=models.CASCADE, related_name='assessment_mappings')
    marks_allocated = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('assessment', 'clo')
    
    def __str__(self):
        return f"{self.assessment.title} → {self.clo.title}"


class AssessmentResult(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assessment_results')
    marks_obtained = models.IntegerField(validators=[MinValueValidator(0)])
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    graded_date = models.DateTimeField(blank=True, null=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_assessments')
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('assessment', 'student')
    
    def save(self, *args, **kwargs):
        if self.marks_obtained is not None and self.assessment.max_marks > 0:
            self.percentage = (self.marks_obtained / self.assessment.max_marks) * 100
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.student_id} - {self.assessment.title}"


# ============================================================================
# SURVEYS
# ============================================================================

class Survey(models.Model):
    SURVEY_TYPE_CHOICES = [
        ('feedback', 'Feedback'),
        ('assessment', 'Assessment'),
        ('satisfaction', 'Satisfaction'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]
    
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='surveys')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    survey_type = models.CharField(max_length=20, choices=SURVEY_TYPE_CHOICES, default='feedback')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_surveys')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.course_offering.course.code})"


class SurveyQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('likert', 'Likert Scale'),
        ('text', 'Text'),
        ('rating', 'Rating'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='likert')
    order_index = models.IntegerField(default=0)
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order_index']
    
    def __str__(self):
        return f"Q{self.order_index}: {self.question_text[:50]}"


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='survey_responses')
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('survey', 'student')
    
    def __str__(self):
        return f"{self.student.student_id} → {self.survey.title}"


class SurveyQuestionResponse(models.Model):
    survey_response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='question_responses')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)
    answer_value = models.IntegerField(blank=True, null=True)  # For numeric responses
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.survey_response} → Q{self.question.order_index}"
