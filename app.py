import flask
import pymongo

import forms
import database
import libuser
import libpost


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '145606a433bb166bfe1086816a42eba746af1a498f88fc094a13f4cbba43cb08'

Cluster0 = None
db = None
try:
    Cluster0 = pymongo.MongoClient("mongodb://Fotonque:BxCKoHUuMc4y2meB@fotondb-shard-00-00.jxjyx.mongodb.net:27017,fotondb-shard-00-01.jxjyx.mongodb.net:27017,fotondb-shard-00-02.jxjyx.mongodb.net:27017/flask_db?ssl=true&replicaSet=FotonDB-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = database.Database(Cluster0)
    print("Cluster connection: success")
except:
    print("Cluster connection: error occurred")

posts = [
    {
        'author': 'qwer',
        'title': 'qwer',
        'content': 'This property specifies whether the current rendered line should break if the content exceeds the boundary of the specified rendering box for an element (this is similar in some ways to the ‘clip’ and ‘overflow’ properties in intent.) This property should only apply if the element has a visual rendering, is an inline element with explicit height/width, is absolutely positioned and/or is a block element',
        'date_posted': 'qwer'
    },
    {
        'author': 'qwer',
        'title': 'qwer',
        'content': 'qwer',
        'date_posted': 'qwer'
    },
    {
        'author': 'qwer',
        'title': 'qwer',
        'content': 'qwer',
        'date_posted': 'qwerq'
    }
]

@app.route('/')
@app.route('/index.html')
def index():
    return flask.render_template('index/index.html')

@app.route('/news.html')
def news():
    return flask.render_template('news/news.html', posts = posts)

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if flask.request.method == 'POST':
        if form.validate_on_submit():
            print(form.username)
            print(form.email)
            print(form.password)
            print(form.confirmPassword)

            user = libuser.User(
                form.username.data,
                form.password.data,
                form.email.data
            )

            result = db.insert_user(user)
            print(result)
            if result == db.SUCCESS:
                flask.flash('Account created', 'success')
                print("Account has been created")
                print(user.login, user.password, user.email)
                return flask.redirect(flask.url_for('index'))
            else:
                flask.flash(u'Account creation error', 'error')
                flask.flash(u'Login already exist in database', 'error')
                print("Login already exist in database")
            
    return flask.render_template('register/register.html', form = form)

@app.route('/login.html', methods=['GET', 'POST'])
def loginIn():
    form = forms.LoginForm
    if flask.request.method == 'POST':
        if form.validate_on_submit():
            return flask.redirect(flask.url_for('index'))
    else:
        return flask.render_template('login/login.html', form = form)

if __name__ == "__main__":
    app.run(debug=True)