import flask_wtf
import wtforms

class RegistrationForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', 
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Length(min = 3, max = 20)])
    email = wtforms.StringField('Email',
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Email()])
    
    #password = wtforms.PasswordField('New Password')
    #confirmPassword  = wtforms.PasswordField('Repeat Password')
    password = wtforms.PasswordField('Password',
        validators=[wtforms.validators.DataRequired()])
    
    confirmPassword = wtforms.PasswordField('Confirm_password',
        validators=[wtforms.validators.DataRequired(), wtforms.validators.equal_to('password', message='Passwords must match')])
    submit = wtforms.SubmitField('Sign up')

class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', 
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Length(min = 3, max = 20)])
    password = wtforms.PasswordField('Password',
        validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Sign_up')

class PostForm(flask_wtf.FlaskForm):
    title = wtforms.StringField('Title',
        validators=[wtforms.validators.DataRequired()])
    content = wtforms.StringField('Content',
        validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Create')