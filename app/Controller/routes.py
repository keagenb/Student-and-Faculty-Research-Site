from __future__ import print_function
import sys
from typing import Text
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from flask_login import login_required, current_user


from app import db
from app.Model.models import Language, Post, User, Research, Apply
from app.Controller.forms import ApplicantsForm, PositionForm, EditForm, SetupForm, ApplyForm, SortForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


#Landing page w/ links to sign in or register
@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    else:
        return render_template('index.html', title="Welcome")

#How to restrict page access by user: 
#   user = current_user
#   if user.usertype == 'student' (or if user.usertype == 'faculty'):
#   issue flash message
#   redirect to another page if they should not be allowed to view it
#   else:
#   do normal thing for that route
# 
#   feel free to use the facultyTest and studentTest html templates if you want to mess around with this


#Home page, displays all research positions
#Source for sorting by tags: https://docs.sqlalchemy.org/en/14/orm/tutorial.html

@bp_routes.route('/home', methods=['GET','POST'])
@login_required
def home():
    user = current_user

    #Used to gather user input
    sform = SortForm()

    #Used to sort the posts based on input
    date = sform.date.data
    topic = sform.rTopics.data
    language = sform.language.data
    myPosts = sform.myposts.data
    reset = sform.reset.data
    recc = sform.recommended.data

    #Default if not sorting is applied
    position = Post.query.order_by(Post.date1.desc())

    #Sorting posts

    if sform.validate_on_submit():
        position = sort(date,topic,language,myPosts)

        if reset == True:
            return redirect(url_for('routes.home'))
        
        if recc != 'Show all posts':
            position = recommended(recc)

    return render_template('home.html', title="Home", posts=position.all(), totalPosts=position.count(), form = sform, user=user)

def sort(d, t, l, myP):
    if d == 'Select Date':
        d = Post.date1.desc()
    if d == 'Newest':
        d = Post.date1.desc()
    if d == 'Oldest':
        d = Post.date1

    #Sorting by user posts only
    if myP == True:

        if t == 'Select Topic':
            if l == 'Select Language':
                position = current_user.get_user_posts().order_by(d)
                return position
            else:
                position=current_user.get_user_posts().filter(Post.language_field.any(Language.field==l)).order_by(d)
                return position
        
        if l == 'Select Language':
            if t == 'Select Topic':
                position = current_user.get_user_posts().order_by(d)
            else:
                position=current_user.get_user_posts().filter(Post.research_field.any(Research.field==t)).order_by(d)
                return position

        #If no filters are applied, display all
        position = current_user.get_user_posts().filter(Post.research_field.any(Research.field==t)).filter(Post.language_field.any(Language.field==l)).order_by(d)
        return position

    #Default for if all filters have a selection
    position = Post.query.filter(Post.research_field.any(Research.field==t)).filter(Post.language_field.any(Language.field==l)).order_by(d)

    if t == 'Select Topic':
        if l == 'Select Language':
            position = Post.query.order_by(d)
            return position
        else:
            position = Post.query.filter(Post.language_field.any(Language.field==l)).order_by(d)
            return position

    if l == 'Select Language':
        if t =='Select Topic':
            position = Post.query.order_by(d)
            return position
        else:
            position = Post.query.filter(Post.research_field.any(Research.field==t)).order_by(d)
            return position
    
    return position

def recommended(r):
    user = current_user
    languages = ['x','x','x','x']  #array to store languages w/buffer
    topics = ['x','x','x','x'] #array to store topics
    i = 0

    position = Post.query.order_by(Post.date1.desc())

    #This works, but only filters by the last tag associated with the user since it keeps resorting, not multisorting

    for lang in user.get_user_lang().all():
        languages.insert(i,lang.field)
        i = i+1

    i = 0
    for topic in user.get_user_tags().all():
        topics.insert(i,topic.field)
        i = i+1
    
    
    l1 = str(languages[0])
    l2 = str(languages[1])
    l3 = str(languages[2])
    l4 = str(languages[3])
    l5 = str(languages[4])

    t1 = str(topics[0])
    t2 = str(topics[1])
    t3 = str(topics[2])
    t4 = str(topics[3])
    t5 = str(topics[4])

    print(languages)
    print(topics)  

    if r == 'Show recommended topics':
        position = Post.query.filter(
        Post.research_field.any(Research.field==t5)) and Post.query.filter(
        Post.research_field.any(Research.field==t4)) and Post.query.filter(
        Post.research_field.any(Research.field==t3)) and Post.query.filter(
        Post.research_field.any(Research.field==t2)) and Post.query.filter(
        Post.research_field.any(Research.field==t1))

    if r == 'Show recommended languages':
        position = Post.query.filter(
            Post.language_field.any(Language.field==l5)) and Post.query.filter(
                Post.language_field.any(Language.field==l4)) and Post.query.filter(
                Post.language_field.any(Language.field==l3)) and Post.query.filter(
                Post.language_field.any(Language.field==l2)) and Post.query.filter(
                Post.language_field.any(Language.field==l1))

    return position

#IMPORTANT
# To change the topics and languages that appear, go to research.py and edit them manually in line 15
# Be sure to delete db file everytime you do this since you are editing the db schema, otherwise it will not appear

@bp_routes.route('/post', methods=['GET','POST'])
@login_required
def post():
    user = current_user
    if user.usertype == 'student':
        return redirect(url_for('routes.home'))
    else:
        hform = PositionForm()
        if user.firstname is None:
                flash('Please finish setting up your profile before creating a position')
                return redirect(url_for('routes.edit'))
        if hform.validate_on_submit():
            newpost = Post(project_title = hform.project_title.data,
            description = hform.description.data,
            date1 = hform.date1.data,
            date2 = hform.date2.data,
            time = hform.time.data,
            requirements = hform.requirements.data, 
            faculty_info = user.firstname + ' '+ user.lastname + ' ' +user.email + ' ' +str(user.phone),
            user_id=current_user.id)
            research_field = hform.research.data
            for t in research_field:
                newpost.research_field.append(t)
            language_field = hform.language.data
            for l in language_field:
                newpost.language_field.append(l)
            db.session.add(newpost)
            db.session.commit()
            flash('Research position '+ newpost.project_title + ' has been posted')
            return redirect(url_for('routes.home'))
        return render_template('_post.html', title="Home", form=hform)

#Should probably move below to auth routes

@bp_routes.route('/setup', methods=['GET','POST'])
@login_required
def setup():
    eform = SetupForm()
    user = current_user
    if user.usertype=='student':
        if eform.validate_on_submit():
            user.firstname=eform.firstname.data
            user.lastname=eform.lastname.data
            user.phone=eform.phone.data
            user.gpa=eform.gpa.data
            user.major=eform.major.data
            user.graduation=eform.graduation.data
            user.experience=eform.experience.data

            research_field = eform.research.data
            for t in research_field:
                user.research_field.append(t)
            language_field = eform.language.data
            for l in language_field:
                user.language_field.append(l)

            db.session.add(user)
            db.session.commit()
            flash("Your account has been updated")
            return redirect(url_for('routes.home'))
    if user.usertype=='faculty':
        flash("You must be a student to view this page")
        return redirect(url_for('routes.home'))

    return render_template('setup.html', form = eform)

@bp_routes.route('/edit', methods=['GET','POST','DELETE'])
@login_required
def edit():
    eform = EditForm()
    user=current_user
    if request.method == 'POST': #For updating\
        if eform.validate_on_submit():
            user.firstname=eform.firstname.data
            user.lastname=eform.lastname.data
            user.phone=eform.phone.data
            user.gpa=eform.gpa.data
            user.major=eform.major.data
            user.graduation=eform.graduation.data
            user.experience=eform.experience.data

            #remove tags otherwise more will just be added to existing
            if user:
                research_field=user.research_field.all()
                for t in research_field:
                    user.research_field.remove(t)
                db.session.commit()

                language_field=user.language_field.all()
                for t in language_field:
                    user.language_field.remove(t)
                db.session.commit()

            research_field = eform.research.data
            for t in research_field:
                user.research_field.append(t)
            language_field = eform.language.data
            for l in language_field:
                user.language_field.append(l)

            db.session.add(user)
            db.session.commit()
            flash("Your account has been updated")
    if request.method == 'GET': #For autofilling info
        eform.firstname.data=user.firstname
        eform.lastname.data=user.lastname
        eform.phone.data=user.phone
        eform.gpa.data=user.gpa
        eform.major.data=user.major
        eform.graduation.data=user.graduation
        eform.experience.data=user.experience
    return render_template('myprofile.html', form = eform, user=user)

@bp_routes.route('/apply/<postid>', methods=['POST'])
@login_required
def applyPost(postid):
    post = Post.query.filter_by(id=postid).first()
    if not current_user.is_applied(post):
        applyform = ApplyForm()
        if applyform.validate_on_submit():
            current_user.apply(post)
            current_user.set_statement(post, applyform.statement.data)
            current_user.set_reference(post, applyform.reference.data)
            flash('You applied to {}!'.format(post.project_title))
            return redirect(url_for('routes.home'))
        return render_template('apply.html', form = applyform, post = post)
    else:
        flash("You already applied to this application!")
        return redirect(url_for('routes.home'))

@bp_routes.route('/withdraw/<postid>', methods = ['POST'])
@login_required
def withdrawPost(postid):
    post = Post.query.filter_by(id=postid).first()
    if current_user.is_applied(post):
        current_user.withdraw(post)
        db.session.commit()
        flash('You have successfully withdrawed from {}!'.format(post.project_title))
        return redirect(url_for('routes.index'))
    else:
        flash('You have not applied to this application!')

@bp_routes.route('/submittedapps', methods=['GET'])
@login_required
def submittedapps():
    print(current_user.applied_apps())
    #print(current_user.applied_apps().appenrolled)
    if None in current_user.applied_apps():
        print("~-~||NO APPS FOUND")
    elif current_user.applied_apps() != []:
        return render_template('submittedapps.html')
    else:
        flash('You have not submitted any applications!')
    return redirect(url_for('routes.index'))

@bp_routes.route('/receivedapps', methods=['GET', 'SET'])
@login_required
def receivedapps():
    applicantform = ApplicantsForm()
    # Testing a check for applications matching to faculty's posts
    mypostids = []
    print("User Post ID's: ")
    for post in current_user.get_user_posts():
        print(post.id)
        mypostids.append(post.id)
    # Testing 'facultyinfo' field from apply model compared to combination of user model info
    print("{} {} {} {}".format(current_user.firstname, current_user.lastname, current_user.email, current_user.phone))
    # Printing all applications iterating through student users
    for student in User.query.filter_by(usertype='student'):
        print(student.firstname, student.lastname)
        for application in student.apps:
            print(application.studentenrolled)
    print()
    # Testing it all together. Displaying the application name and student name for all applications for the current faculty user
    print("User Applicants: ")
    for app in Apply.query.all():
        if app.appid in mypostids:
            print("Application {}:".format(app.appid))
            print("Student: {}".format(User.query.filter_by(id = app.studentid).first().firstname))

    if (Apply.query.count() > 0):
        return render_template('receivedapps.html', form = applicantform)
    else:
        flash('You have not received any applications!')
    return redirect(url_for('routes.index'))

@bp_routes.route('/status/<app_id><student_id>', methods=['SET', 'GET', 'POST'])
@login_required
def status(app_id, student_id):
    applicantform = ApplicantsForm()
    #app = Apply.query.filter_by(appid=app_id).first()
    post = Post.query.filter_by(id=app_id).first()
    student = User.query.filter_by(id=student_id).first()
    app = Apply.query.filter_by(studentid=student.id).first()
    print("~-~-|| STUDENT NAME ||-~-~")
    print(student.firstname)
    print(applicantform.status.data)
    print("Before applyform validate")
    if applicantform.validate_on_submit:
        print()
        print("Status Testing:")
        print(applicantform.status.data)
        #if applicantform.status.data == '1':
        app.studentenrolled.set_status(post, applicantform.status.data)
        db.session.commit()
        flash('You have updated the status for ' + app.studentenrolled.firstname + ' ' + app.studentenrolled.lastname)
        return redirect(url_for('routes.receivedapps'))
    return render_template('receivedapps.html', form = applicantform)

@bp_routes.route('/delete/<post_id>', methods=['DELETE', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.filter_by(id = post_id).first()
    app = Apply.query.filter_by(appid=post.id).first()
    student = User.query.filter_by(id=app.studentid).first()
    if (post):
        student.withdraw(post)
        db.session.delete(post)
        db.session.commit()
        flash ('Posting "' + post.project_title + '"has been deleted.')
        return redirect(url_for('routes.home'))
        