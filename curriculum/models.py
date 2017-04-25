import datetime
from django.db import models
from django.utils import timezone
from django.db.models import Q

class Lars(models.Model):
    qual_aim = models.CharField(max_length=10, primary_key=True)
    qual_aim_title = models.CharField(max_length=100)
    def __str__(self):
        return self.qual_aim

class Offering(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_rpt = models.BooleanField(default=False)
    course_caution = models.BooleanField(default=False)
    course_complete = models.BooleanField(default=False)
    course_code = models.CharField(max_length=20, blank=True)
    course_code_old = models.CharField(max_length=20, blank=True)
    course_name = models.CharField(max_length=200, help_text="Enter a name that makes sense")
    DELIVERY_CHOICES = (
        ('FT', 'Full Time'),
        ('PTQ', 'Part Time Qualification'),
        ('HE', 'Higher Education'),
        ('L2L', 'Love2Learn'),
        ('APP', 'Apprenticeship'),
        )
    course_delivery = models.CharField(max_length=100, choices=DELIVERY_CHOICES, default='FT')
    TYPE_CHOICES = (
        ('M', 'Main Aim'),
        ('N', 'Nested Qualification'),
        ('C', 'Child Code'),
        ('S', 'Standalone Course'),
        ('F', 'Functional Skills'),
        ('G', 'Group Code'),
        ('R', 'Register Code'),
        )
    course_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='M')
    parent_code = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    STRAND_CHOICES = (
        ('A2H', 'Access to HE'),
        ('ACC', 'Accommodation'),
        ('AHC', 'Animal Care'),
        ('APP', 'Apprenticeships'),
        ('ART', 'Arts'),
        ('ASC', 'Ascentis'),
        ('BEA', 'Beauty'),
        ('BER', 'Business Employer Responsive'),
        ('BLS', 'Building Services Engineering'),
        ('BRI', 'Bricklaying'),
        ('BUS', 'Business'),
        ('CAD', 'Careers Advice & Guidance'),
        ('CAR', 'Care'),
        ('CON', 'Construction (Somer Valley)'),
        ('CPT', 'Carpentry'),
        ('CST', 'Construction  CIBE'),
        ('CVC', 'Cardiff and Vale College'),
        ('DEU', 'Distance Education'),
        ('DLH', 'Distance Learning (Highways/ILM)'),
        ('DNG', 'Design'),
        ('DWA', 'Development Worker A'),
        ('ELI', 'Electrical'),
        ('ELS', 'English Language School (inc. ESOL)'),
        ('ELY', 'Early Years'),
        ('ENG', 'Engineering'),
        ('EXM', 'Exam Resiit Fees'),
        ('FDN', 'Foundation Learning'),
        ('FIN', 'Finance'),
        ('FLO', 'Floristry'),
        ('GCS', 'GCSEs'),
        ('HAB', 'Hair & Beauty'),
        ('HAI', 'Hair'),
        ('HOR', 'Horticulture'),
        ('HOS', 'Hospitality'),
        ('INT', 'Information Technology'),
        ('LCV', 'Learning Curve'),
        ('MED', 'Media'),
        ('MFL', 'Modern Foreign Languages'),
        ('MOT', 'Motor Vehicle'),
        ('MRK', 'Marketing'),
        ('MTD', 'Business Professional'),
        ('MUS', 'Music'),
        ('NCC', 'NCC Skills Ltd'),
        ('NGT', 'N-Gaged Training'),
        ('ODC', 'One Day Course'),
        ('OTH', 'Other Miscellaneous Codes'),
        ('PAD', 'Painting & Decorating'),
        ('PAR', 'Performing Arts'),
        ('PBS', 'Public Services'),
        ('PMB', 'Plumbing'),
        ('PRE', 'Pre-16'),
        ('PRM', 'Premier'),
        ('REF', 'Refrigeration'),
        ('SAA', 'Strand Area A'),
        ('SAB', 'Strand Area B'),
        ('SAC', 'Student Advice Centre'),
        ('SFL', 'Skills for Life'),
        ('SHC', 'Short Courses'),
        ('SPO', 'Sport'),
        ('STO', 'Stonemasonry'),
        ('T2G', 'Train to Gain'),
        ('TAS', 'Teaching Assistants'),
        ('TNT', 'Travel & Tourism'),
        ('TRP', 'Traineeship'),
        ('TTR', 'Teacher Training'),
        ('UFU', 'Units for the Unemployed'),
        ('UOB', 'UoB International Foundation Year'),
        ('UOL', 'UoL BSC Business'),
        ('VAP', 'Vocational Access Programme'),
        ('VET', 'Veterinary Nursing'),
        ('XLR', 'Pre-16'),
        )
    strand = models.CharField(max_length=100, choices=STRAND_CHOICES, default='A2H')
    DEPT_CHOICES = (
        ('DACL', 'Dept of Adult and Community Learning'),
        ('DCAE', 'Dept of Creative Arts and Enterprise'),
        ('DEAM', 'Dept of English & Maths'),
        ('DECC', 'Dept of Technology'),
        ('DFDN', 'Dept of Foundation Learning'),
        ('DHBS', 'Dept of Hospitality, Hair, Beauty and Spa Industries'),
        ('DINT', 'Dept for International Studies'),
        ('DLBS', 'Dept of Land Based Studies'),
        ('DSLC', 'Dept of Sport, Leisure & Care'),
        ('DSTB', 'Dept of Services to Business & Work Based Learning'),
        ('DXDY', 'Dept of Specialist Delivery'),
        ('MISC', 'Miscellaneous Codes & Fees (Agresso)'),
        )
    department = models.CharField(max_length=100, choices=DEPT_CHOICES, default='DACL')
    SITE_CHOICES = (
        ('CC','Bath - City Centre Campus'),
        ('SV','Radstock - Somer Valley Campus'),
        ('XX','Cross-College'),
        ('EE','External / Employer'),
        )
    location = models.CharField(max_length=100, choices=SITE_CHOICES, default='CC')
    qual_aim = models.CharField(max_length=10, null=True)
    qual_aim_title = models.ForeignKey(Lars, null=True, on_delete=models.SET_NULL)
    fee_comments = models.CharField(max_length=250)
    start_date = models.DateField
    end_date = models.DateField
    start_time = models.TimeField
    end_time = models.TimeField
    day = models.CharField(max_length=100)
    study_year = models.IntegerField(help_text="For courses with a duration of one year or less, this will always be '1'")
    study_year_duration = models.IntegerField(help_text="How many years will this course take overall?")


    def __str__(self):
        return self.course_name + ' - ' + self.course_code


"""
    wk_hrs (how many hours does this aim require per week?)
    number_wks (how many weeks does this aim run for?)
    glh (total guided learning hours, inc. teaching and tutorials, does NOT include employability)
    number_grps (how many groups will be required?)
    min_students (minimum number of students required for course to run / be viable)
    max_students (maximum number of students that can be taught - total, not per group)
    tuition_fee
    tuition_fee_old (only assigned if user selects repeat course option, used by Finance to assist in planning fees)
    exam_fee
    exam_fee_old (only assigned if user selects repeat course option, used by Finance to assist in planning fees)
    materials_fee
    materials_fee_old (only assigned if user selects repeat course option, used by Finance to assist in planning fees)
    other_fee
    other_fee_old (only assigned if user selects repeat course option, used by Finance to assist in planning fees)
    fcr_fee (full cost recovery fee - i.e. how much a student pays if they receive no funding at all)
    fcr_fee_old (only assigned if user selects repeat course option, used by Finance to assist in planning fees)
    weighted_matrix (weighted matrix funding amount, based on lars lookup via qual_aim)
    mkt_course_name (attractive, readable course title for printing in prospectus)
    mkt_course_overview (blurb for prospectus / web)
    mkt_prospectus (list of prospectuses that course should appear in - can be None)
    mkt_entry_req (entry requirements, if any)
    mkt_topics (topics of study that are covered)
    mkt_target (who is the course aimed at?)
    mkt_learning (what are the learning / delivery methods? how will you learn?)
    mkt_assess (what are the assessment methods? how will you be assessed?)
    mkt_career (what are your progression options? what career path might you follow by enrolling on this course?)
    mkt_funding (what funding options are available?)
    mkt_add_costs (are there any additional costs?)
    mkt_where (where will you go on your first day?)
    mkt_bring (what do I need to bring?)
    mkt_other (what else do I need to know? anything else / extra?)
    mkt_tutor
"""
