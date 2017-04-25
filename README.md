# Planr Documentation

<a href="introduction.md">Read the non-technical guide here</a>

## Contents
<a href="#versions">Versions</a> | <a href="#hosting">Hosting</a> | <a href="#app-structure">App Structure</a> | <a href="#user-interface">User Interface</a> | <a href="#filtering-and-presentation-of-data">Filtering Data</a> | <a href="#data-validation">Data Validation</a> | <a href="#custom-user-model">Custom User Model</a> | <a href="#offering-model">Offering Model</a> | <a href="#lars-model">LARS Model</a> | <a href="#parent--child-codes">Parent / Child Codes</a> | <a href="#user-groups">User Groups</a> | <a href="#user-resources">User Resources</a> | <a href="#css-and-js">CSS and Javascript</a>

## Overview

### Versions
I am currently using Python 3.6.1 and Django 1.11 for my development trials, although I have not properly begun writing the final application code yet. Core Django documentation is available <a href="https://docs.djangoproject.com/en/1.11/">here</a>.

### Hosting
If possible, I will aim to host the webapp on the college's servers, which I think run nginx, and should therefore be compatible. However, if this is not feasible, or there is too much set up required (I'm not really savvy on server management / sysadmin), then I may use a separate host. The current leader is www.hostpresto.com, who are based in the UK, offer a low priced option (£3.50 per month), and have support for Django installations. Another possibility is www.pythonanywhere.com, who offer a very streamlined Django set-up, but are slightly more expensive.

### App Structure
It should be a relatively small and simple application, with three app folders: planr (the main system files); curriculum (the core templates, models, and views), and custom_user (for building the user model).

Three models will be specified in **curriculum**: offering; old_offering; lars. The new curriculum will be built in the offering model/table, while the old_offering table will act as a point of reference if users want to repeat a course. The lars table will provide fee and funding information and will be linked to the offering table via the learning aim; up to date LARS data can be downloaded from <a href="https://hub.fasst.org.uk/Learning%20Aims/Downloads/Pages/default.aspx">here</a>.

### User Interface
The goal is to create something ridiculously simple, which facilitates joint access to a core database without cluttering up the screen with information not relevant to the user. Marketing should not have to see GLH or fee comments, but will need to know what prospectus the course should be advertised in; Finance will need to see fee comments from the department, but not timetabling information.

The UI will prevent users from making changes to the overall structure, and will include validation and warnings if a course is not properly completed. Academic users will be able to set caution flags if a course is pending approval, and an approved flag if they are happy with the information provided.

Academic users will be able to create a new course, in which case all relevant fields will be blank by default, or they can opt to repeat an offering from the previous academic year. If they choose this option, once the 'old' course is selected, the fields will have suggestions next to them, which can be copied over by clicking a 'copy' button. This saves time for the staff inputting the data, but means there is still oversight and they have to visually validate the data (additional data validation will still be built into the form to catch incorrect dates etc.).

Using this repeat offering function will also set the course_rpt flag to `True`, and store the old course code and old fee information (although this will not be visible to the academic staff inputting the course).

### Filtering and presentation of data
The underlying offering table will contain everything, but not everyone will want to see everything, and in particular different departments should not see or be able to edit each other's courses.

At present, there are two filtering methods that have been tested and should work well in conjunction.

In curriculum.views.py the IndexView can use a series of filters that examine the user's credentials in order to present a filtered list of data to the index template:

```python
def get_queryset(self):
    if self.request.user.dept.startswith('D'):
        data = Offering.objects.filter(department__icontains=self.request.user.dept)
    elif self.request.user.dept == 'LV2L':
        data = Offering.objects.filter(course_delivery__icontains=self.request.user.dept)
    else: data = Offering.objects.all()
        return data
```

A further filter is then applied in the index template using a custom filter in curriculum/templatetags/curriculum_extra.py, which examines the user's group (rather than their department):

```python
from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
```

This is then called in the template file using the following method:

```python
{% if request.user|has_group:"Marketing" %}
<table>{{ offering data }}</table>
{% endif %}


{% if request.user|has_group:"Academic" %}
<table>{{ offering data }}</table>
{% endif %}
```

Each has_group query condition will display a different subset of fields, and provided the tailored interface best suited to each team.

A link should be clearly visible at all times so that users can export their data to Excel or similar. It is not recommended that they work on the data offline, but chances are someone will want to be able to do it, so it's probably better to provide them with the function.

### Data Validation
Where possible, the data that users input should be validated during entry, so that mistakes are caught early. It should be possible to use regular expressions and javascript to assess the information being provided. Key areas are dates and times.

It may also be possible to 'recommend' values for some fields. For instance, if a user provides a start date of 07/09/17, and an end date of 24/05/18, a relatively simple calculation can suggest 32 weeks for the **number_wks** field; if the weekly hours are then provided, the GLH can also be recommended. These suggestions can still be overridden / ignored, but the automation should help to improve the user experience.

### Custom User Model
The reasons for including a custom user model are:<br>
a) users can use their email address instead of a username: simpler and easier<br>
b) additional fields can be added - in particular the department that is crucial to filtering the displayed data

At present the fields will be:<br>
**email**<br>
**first_name**<br>
**last_name**<br>
**dept**

### Offering Model
At present the fields will be:<br>
**course_id** (auto-increment, automatically assigned primary key)<br>
**course_rpt** (boolean, automatically set to True if user selects `repeat course` option)<br>
**course_caution** (boolean, flag to highlight courses that are subject to possible deletion)<br>
**course_complete** (boolean, flag to highlight when academic staff are confident that course is ready for finance / marketing)<br>
**course_code** (not displayed to academic staff, assigned by CIS, viewable by Marketing)<br>
**course_code_old** (only assigned if user selects `repeat course` option, used by Marketing to assign in uploading to web)<br>
**course_name** (ProSolution course name, can be technical / shortened)<br>
**course_delivery** (full time, part time, L2L, apprenticeship, HE)<br>
**course_type** (main aim, nested qual, child code)<br>
**parent_code** (if nested or child, can select from list of offerings in offering table)<br>
**strand**<br>
**department**<br>
**location** (campus / site)<br>
**qual_aim**<br>
**qual_aim_title** (automatically assigned via lars table lookup based on provided qual_aim)<br>
**fee_comments** (allows academic staff to record useful information for Finance so that fees can be planned correctly)<br>
**start_date**<br>
**end_date**<br>
**start_time**<br>
**end_time**<br>
**day**<br>
**study_year** (which year of study does this represent?)<br>
**study_year_duration** (how many years does the course take overall?)<br>
**wk_hrs** (how many hours does this aim require per week?)<br>
**number_wks** (how many weeks does this aim run for?)<br>
**glh** (total guided learning hours, inc. teaching and tutorials, does NOT include employability)<br>
**number_grps** (how many groups will be required?)<br>
**min_students** (minimum number of students required for course to run / be viable)<br>
**max_students** (maximum number of students that can be taught - total, not per group)<br>
**tuition_fee**<br>
**tuition_fee_old** (only assigned if user selects `repeat course` option, used by Finance to assist in planning fees)<br>
**exam_fee**<br>
**exam_fee_old** (only assigned if user selects `repeat course` option, used by Finance to assist in planning fees)<br>
**materials_fee**<br>
**materials_fee_old** (only assigned if user selects `repeat course` option, used by Finance to assist in planning fees)<br>
**other_fee**<br>
**other_fee_old** (only assigned if user selects `repeat course` option, used by Finance to assist in planning fees)<br>
**fcr_fee** (full cost recovery fee - i.e. how much a student pays if they receive no funding at all)<br>
**fcr_fee_old** (only assigned if user selects `repeat course` option, used by Finance to assist in planning fees)<br>
**weighted_matrix** (weighted matrix funding amount, based on lars lookup via qual_aim)<br>
**mkt_course_name** (attractive, readable course title for printing in prospectus)<br>
**mkt_course_overview** (blurb for prospectus / web)<br>
**mkt_prospectus** (list of prospectuses that course should appear in - can be `None`)<br>
**mkt_entry_req** (entry requirements, if any)<br>
**mkt_topics** (topics of study that are covered)<br>
**mkt_target** (who is the course aimed at?)<br>
**mkt_learning** (what are the learning / delivery methods? how will you learn?)<br>
**mkt_assess** (what are the assessment methods? how will you be assessed?)<br>
**mkt_career** (what are your progression options? what career path might you follow by enrolling on this course?)<br>
**mkt_funding** (what funding options are available?)<br>
**mkt_add_costs** (are there any additional costs?)<br>
**mkt_where** (where will you go on your first day?)<br>
**mkt_bring** (what do I need to bring?)<br>
**mkt_other** (what else do I need to know? anything else / extra?)<br>
**mkt_tutor** (who is the tutor for this course? what are their credentials?)<br>

### LARS Model
I will need to check with Finance to see which pieces of information are useful, but the obvious fields are:<br>
**lars_id** (pk)<br>
**qual_aim**<br>
**qual_aim_title**<br>
**weighted_matrix**<br>

### Parent / Child codes
This year it was possible for academic staff to enter parent / programme details, but it was inconsistently applied, and is probably something that should be assigned by CIS outside of the curriculum planning process. At present, FT programme codes are created before their main aim codes anyway, as they serve the dual purpose of receiving applications and grouping offerings.

However, this is not the only instance of parent / child relationshipss; it will be necessary to link M and C codes in this way. A drop-down menu will allow the user to assign a parent code from the list of already created codes in the offering table. This will only appear if the course_type is set to Nested Qual or Child.

### User Groups
The following user groups will be defined, which can be chosen during account creation. Once set, there is no reason that this should change (assuming that users choose correctly).<br>
ACDM - Academic<br>
MKTG - Marketing<br>
FNCE - Finance<br>
LV2L - Love2Learn<br>
RGST - Registers<br>
PRMS - Premises<br>
OTHR - Other

#### Academic
This group will allow users to then choose from the following departments:<br>
DACL - Adult and Community Learning<br>
DEAM - English and Maths<br>
DECC - Technology<br>
DCAE - Creative Arts and Enterprise<br>
DFDN - Foundation Learning<br>
DHBS - Hospitality, Hair, Beauty and Spa Industries<br>
DINT - International Studies<br>
DLBS - Landbased Studies<br>
DSLC - Sport, Leisure and Care<br>
DSTB - Services to Business and Work-based Learning<br>
DXDY - Specialist Delivery

Academic users should have access to:<br>
**course_name**<br>
**course_caution**<br>
**course_complete**<br>
**course_delivery**<br>
**course_type**<br>
**parent_code**<br>
**strand**<br>
**department**<br>
**location**<br>
**qual_aim**<br>
**qual_aim_title**<br>
**fee_comments**<br>
**start_date**<br>
**end_date**<br>
**start_time**<br>
**end_time**<br>
**day**<br>
**study_year**<br>
**study_year_duration**<br>
**wk_hrs**<br>
**number_wks**<br>
**glh**<br>
**number_grps**<br>
**min_students**<br>
**max_students**<br>
**mkt_course_name**<br>
**mkt_course_overview**<br>
**mkt_prospectus**
**mkt_entry_req**<br>
**mkt_topics**<br>
**mkt_target**<br>
**mkt_learning**<br>
**mkt_assess**<br>
**mkt_career**<br>
**mkt_funding**<br>
**mkt_add_costs**<br>
**mkt_where**<br>
**mkt_bring**<br>
**mkt_other**<br>
**mkt_tutor**

#### Marketing
This group will default into the department `MKTG`. They should have access to the following fields:<br>
**course_rpt**<br>
**course_caution**<br>
**course_complete**<br>
**course_code**<br>
**course_code_old**<br>
**course_name**<br>
**course_delivery**<br>
**strand**<br>
**department**<br>
**location**<br>
**start_date**<br>
**end_date**<br>
**start_time**<br>
**end_time**<br>
**day**<br>
**study_year**<br>
**study_year_duration**<br>
**number_wks**<br>
**min_students**<br>
**max_students**<br>
**tuition_fee**<br>
**exam_fee**<br>
**materials_fee**<br>
**other_fee**<br>
**fcr_fee**<br>
**mkt_course_name**<br>
**mkt_course_overview**<br>
**mkt_prospectus**<br>
**mkt_entry_req**<br>
**mkt_topics**<br>
**mkt_target**<br>
**mkt_learning**<br>
**mkt_assess**<br>
**mkt_career**<br>
**mkt_funding**<br>
**mkt_add_costs**<br>
**mkt_where**<br>
**mkt_bring**<br>
**mkt_other**<br>
**mkt_tutor**<br>

#### Finance
This group will default into the department `FNCE`. They should have access to the following fields:<br>
tbc

#### Love2Learn
This group will default into the department `LV2L`. They should have access to the following fields:<br>
tbc

#### Registers
This group will default into the department `RGST`. They should have access to the following fields:<br>
tbc

#### Premises
This group will default into the department `PRMS`. They should have access to the following fields:<br>
tbc

#### Other
This group will default into the department `OTHR`. They should have access to the following fields:<br>
tbc

### User Resources
Additional resources will be provided for users to help make the site as friendly and straightforward as possible. Some form of timeline or schedule will be helpful so that staff are more clearly aware of when the deadlines are. A reporting function that highlights how many courses in a user's department have been flagged as caution vs complete would be useful.

In an ideal world, there would be a clearly structured timeline that defined the academic planning period, the finance fee planning period, the marketing planning and production period, and the CIS ProSolution validation and import period.

### CSS and JS
In order to style the website, I will use <a href="http://getbootstrap.com/">Bootstrap</a> as it can create a clean and professional look with minimum fuss. The static files for the core CSS will be referenced via a CDN, and custom CSS can be stored on the server (although not in the django-application folder).

CDN links are below:<br>
```html
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
```

<a href="#contents">^ return to top</a><br>
