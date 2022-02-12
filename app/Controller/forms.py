from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField ,validators, DateField, PasswordField, FloatField, IntegerField
from wtforms.fields.core import BooleanField
from wtforms.validators import  DataRequired, Length, Email, EqualTo
from wtforms.widgets.core import TextArea
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from app.Model.models import Research, Language


def get_research():
    return Research.query.all()

def get_researchlabel(theresearch):
    if theresearch.field == 'x':
        theresearch.field = 'Select Topics'
    return theresearch.field

def get_language():
    return Language.query.all()

def get_languagelabel(thelanguage):
    if thelanguage.field == 'x':
        thelanguage.field = 'Select Languages'
    return thelanguage.field


class PositionForm(FlaskForm):
    project_title = StringField('Title of project', validators=[DataRequired()])
    description = TextAreaField('Description of research position', validators = [Length(min=1,max=1500)])
    date1 = DateField('Start date', format='%m/%d/%Y')
    date2 = DateField('End date', format='%m/%d/%Y')
    time = StringField('How many hours would you like to work?', validators = [DataRequired()])
    research = QuerySelectMultipleField('Research Topics', query_factory = get_research, get_label = get_researchlabel, widget = ListWidget(prefix_label=False),option_widget = CheckboxInput())
    language = QuerySelectMultipleField('Programming Languages', query_factory = get_language, get_label = get_languagelabel, widget = ListWidget(prefix_label=False),option_widget = CheckboxInput())
    requirements = StringField('A brief description of the required qualifications', validators=[DataRequired()])
    faculty_info = TextAreaField('Faculty’s name and contact information ')
    submit = SubmitField('Post')


class SetupForm(FlaskForm):
    firstname =  StringField('First Name', validators=[DataRequired()])
    lastname =  StringField('Last Name', validators=[DataRequired()])
    gpa = FloatField('GPA',validators=[DataRequired()])
    phone = IntegerField('Phone Number',validators=[DataRequired()])
    major = StringField('Major',validators=[DataRequired()])
    graduation = DateField('Graduation Date (Month and Year)', format='%m/%Y',validators=[DataRequired()])
    research = QuerySelectMultipleField('Research Topics', query_factory = get_research, get_label = get_researchlabel, widget = ListWidget(prefix_label=False),option_widget = CheckboxInput())
    language = QuerySelectMultipleField('Programming Languages', query_factory = get_language, get_label = get_languagelabel, widget = ListWidget(prefix_label=False),option_widget = CheckboxInput())
    experience = TextAreaField('Experience')
    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    firstname =  StringField('First Name')
    lastname =  StringField('Last Name')
    gpa = FloatField('GPA')
    phone = IntegerField('Phone Number')
    major = StringField('Major')
    graduation = DateField('Graduation Date (Month and Year)', format='%m/%Y')
    research = QuerySelectMultipleField('Research Topics', query_factory = get_research, get_label = get_researchlabel, widget = ListWidget(prefix_label=False),option_widget = CheckboxInput())
    language = QuerySelectMultipleField('Programming Languages', query_factory = get_language, get_label = get_languagelabel, widget = ListWidget(prefix_label=False),option_widget = CheckboxInput())
    experience = TextAreaField('Experience')
    submit = SubmitField('Submit')

class SortForm(FlaskForm):
    date=SelectField(choices=[('Select Date'),('Newest'),('Oldest')]) #Time filters
    rTopics=SelectField(choices=[('Select Topic'),('Topic1'),('Topic2'),('Topic3'),('Topic4'),('Topic5')])#research topic fields
    language=SelectField(choices=[('Select Language'),('Lang1'),('Lang2'),('Lang3'),('Lang4'),('Lang5')])#programming languages
    recommended=SelectField(choices=[('Show all posts'),('Show recommended topics'),('Show recommended languages')])
    myposts=BooleanField('Display my posts only')
    reset = BooleanField("Reset Filters")
    submit=SubmitField('Apply filters')

class ApplyForm(FlaskForm):
    statement =  StringField('Why are you interested in this position?', validators=[Length(min=1,max=400), DataRequired()])
    reference =  StringField('List at least one faculty reference', validators=[DataRequired()])
    apply = SubmitField('Apply')

class ApplicantsForm(FlaskForm):
    status = SelectField(choices=[('Pending'),('Approved for interview!'),('Not fit for role.'),('Not hired'),('Hired!')])
    submit = SubmitField('Update Applicant Status')