from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from marvel_site.forms import UserLoginForm, UserSignupForm
from marvel_site.models import User, db

from flask_login import login_user, logout_user, current_user, login_required

"""
    Note that in the below code,
    some arguments are specified when creating Blueprint objects.
    The first argument, 'site' is the Blueprint's name.
    which flask uses for routing.

    The second argument, __name__, is the Blueprint's import name,
    which flask uses to locate the Blueprint's resources
"""

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)
            # user = User(email,password=password)
            flash(f"You have successfully 'logged in'")
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("You were successfully logged in", 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash("Your email/password is incorrect", 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your form.')

    return render_template('signin.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignupForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            print(email, password)
            user = User(email, first_name, last_name, password=password)
            db.session.add(user)
            db.session.commit()
            flash(f"You have successfully created a user account for {email}.", "user-created")
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please Check your form.')

    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))

