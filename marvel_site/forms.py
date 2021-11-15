from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    # email, password, submit_button
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit_button = SubmitField()

class UserSignupForm(FlaskForm):
    # email, password, submit_button
    first_name = StringField("First Name (Optional)")
    last_name = StringField("Last Name (Optional)")
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit_button = SubmitField()



