import datetime
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.core.urlresolvers import reverse

class Lars(models.Model):
    qual_aim = models.CharField(max_length=10, primary_key=True)
    qual_aim_title = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "LARS Entries"
    def __str__(self):
        return self.qual_aim + ' ' + self.qual_aim_title

class OldOffering(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=20, blank=True)
    course_name = models.CharField(max_length=200, help_text="Enter a name that makes sense")

class Offering(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_rpt = models.BooleanField(default=False)
    course_caution = models.BooleanField("Subject to change?", default=False, )
    course_complete = models.BooleanField(default=False)
    course_code = models.CharField(max_length=20, default="to be assigned")
    course_code_old = models.CharField(max_length=20, blank=True)
    course_name = models.CharField(max_length=200, help_text="Please follow syntax: [Subject][Qualification][Level][(Extra Information)]. E.g. Plumbing Diploma L3 (Day Release)")
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
    qual_aim_title = models.ForeignKey(Lars, null=True, blank=True, on_delete=models.SET_NULL)
    fee_comments = models.CharField(blank=True, null=True, max_length=250)
    start_date = models.DateField(auto_now=False, auto_now_add=False, default="2018-08-01")
    end_date = models.DateField(auto_now=False, auto_now_add=False, default="2019-06-30")
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, default="09:00")
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, default="16:30")
    DAY_CHOICES = (
        ('Various', 'Multiple Days'),
        ('Weds/Thurs/Fri', 'Weds/Thurs/Fri'),
        ('Weds/Fri', 'Weds/Fri'),
        ('Wednesday', 'Wednesday'),
        ('Wed/Thurs', 'Wed/Thurs'),
        ('Tuesday', 'Tuesday'),
        ('Tues/Wed/Thurs/Fri', 'Tues/Wed/Thurs/Fri'),
        ('Tues/Wed/Thurs', 'Tues/Wed/Thurs'),
        ('Tues/Wed', 'Tues/Wed'),
        ('Tues/Thurs', 'Tues/Thurs'),
        ('Tues/Fri', 'Tues/Fri'),
        ('Thursday', 'Thursday'),
        ('Thurs/Sat', 'Thurs/Sat'),
        ('Thurs/Fri', 'Thurs/Fri'),
        ('Sunday', 'Sunday'),
        ('Saturday', 'Saturday'),
        ('Mon-Fri', 'Mon-Fri'),
        ('Monday', 'Monday'),
        ('Mon/Wed', 'Mon/Wed'),
        ('Mon/Tues/Wed/Thurs', 'Mon/Tues/Wed/Thurs'),
        ('Mon/Tues/Fri', 'Mon/Tues/Fri'),
        ('Mon/Tues', 'Mon/Tues'),
        ('Mon/Thurs', 'Mon/Thurs'),
        ('Mon/Fri', 'Mon/Fri'),
        ('Friday', 'Friday'),
        )
    day = models.CharField(max_length=100, choices=DAY_CHOICES, default='Various', help_text="Day or days that course regularly runs. If combination is not in list, use 'Multiple Days' or contact CIS to have it added to the list.")
    study_year = models.IntegerField(default=1, help_text="For courses with a duration of one year or less, this will always be '1'")
    study_year_duration = models.IntegerField(default=1, help_text="How many years will this course take overall?")
    wk_hrs = models.IntegerField(default=0, help_text="How many hours of study per week?")
    number_wks = models.IntegerField(default=0, help_text="How many weeks will this course run for?")
    glh = models.IntegerField(default=0, help_text="Total guided learning hours, including teaching and tutorials; does NOT include employability")
    number_grps = models.IntegerField(default=1, help_text="How many groups will the course need?")
    min_students = models.IntegerField(default=5, help_text="Minimum number of students required for course to run / be financially viable")
    max_students = models.IntegerField(default=0, help_text="Maximum number of students that can be taught - total, not per group")
    tuition_fee = models.IntegerField(default=0, null=True, blank=True)
    tuition_fee_old = models.IntegerField(default=0, null=True, blank=True)
    exam_fee = models.IntegerField(default=0, null=True, blank=True)
    exam_fee_old = models.IntegerField(default=0, null=True, blank=True)
    materials_fee = models.IntegerField(default=0, null=True, blank=True)
    materials_fee_old = models.IntegerField(default=0, null=True, blank=True)
    other_fee = models.IntegerField(default=0, null=True, blank=True)
    other_fee_old = models.IntegerField(default=0, null=True, blank=True)
    fcr_fee = models.IntegerField(default=0, null=True, blank=True)
    fcr_fee_old = models.IntegerField(default=0, null=True, blank=True)
    weighted_matrix = models.IntegerField(default=0, null=True, blank=True)
    mkt_course_name = models.CharField(default="", max_length=250, help_text="A shorter, easily understood title suitable for print and web, avoid technical language and abbreviations")
    mkt_course_overview = models.TextField(default="", help_text="A general overview of the qualification or course")
    PROSPECTUS_CHOICES = (
        ('NONE','None (do not advertise)'),
        ('FT','Full Time Prospectus'),
        ('PT','Part Time / Love2Learn Prospectus'),
        ('AP','Apprenticeship Prospectus'),
        ('FTAP','Full Time and Apprenticeship'),
        ('PTAP','Part Time and Apprenticeship'),
        ('FTPT','Full Time and Part Time'),
        ('ALL','All Prospectuses'),
    )
    mkt_prospectus = models.CharField(max_length=100, choices=PROSPECTUS_CHOICES, default='NONE', help_text="Which prospectuses (if any) would you like this course to appear in?")
    mkt_entry_req = models.TextField(default="", help_text="What are the entry requirements?")
    mkt_topics = models.TextField(default="", help_text="What topics are covered?")
    mkt_target = models.TextField(default="", help_text="Who is the course aimed at?")
    mkt_learning = models.TextField(default="", help_text="What are the learning / delivery methods? How will students learn?")
    mkt_assess = models.TextField(default="", help_text="How will students be assessed?")
    mkt_career = models.TextField(default="", help_text="Where might this course lead? What are the opportunities for progression both within the college and beyond?")
    mkt_funding = models.TextField(default="", help_text="What funding options are available?")
    mkt_add_costs = models.TextField(default="", help_text="Are there any additional costs?")
    mkt_where = models.TextField(default="", help_text="Where will students need to go on their first day?")
    mkt_bring = models.TextField(default="", help_text="What do students need to bring?")
    mkt_other = models.TextField(default="", help_text="What else do students need to know?")
    mkt_tutor = models.TextField(default="", help_text="Who will teach the course? What are their credentials?")

    def get_absolute_url(self):
        return reverse('curriculum:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.course_name + ' - ' + self.course_code
