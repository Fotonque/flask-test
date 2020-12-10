import flask
import flask_login
import pymongo
import datetime

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
login_manager = flask_login.LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.find_user(
        libuser.User(user_id)
    )
    
@app.route('/')
@app.route('/index.html')
def index():
    return flask.render_template('index/index.html')

@app.route('/news.html')
def news():
    posts = []
    db_posts = db.find_lastPosts()
    for post in db_posts:
        posts.append({
                'author': post['Login'],
                'title': post['title'],
                'content': post['content'],
                'date_posted': post['date']
            })
    return flask.render_template('news/news.html', posts = posts)

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if flask_login.current_user.is_authenticated:
        print("yea")
        return flask.redirect(flask.url_for('myProfile'))
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
                flask.flash(u'Account created', 'success')
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
    form = forms.LoginForm()
    if flask.request.method == 'POST':
        if form.validate_on_submit():
            print(form.username)
            print(form.password)

            user = libuser.User(
                form.username.data,
                form.password.data
            )
            result = db.check_credentials(user)
            if result:
                flask_login.login_user(user, remember=False)
                print(result)
                return flask.redirect(flask.url_for('myProfile'))
            else:
                flask.flash(u'Account not found', 'error')
                flask.flash(u'Credentials are wrong', 'error')

    return flask.render_template('login/login.html', form = form)

@app.route('/profile.html', methods=['GET', 'POST'])
@flask_login.login_required
def myProfile():
    form = forms.PostForm()
    currentUser = flask_login.current_user
    print(form.title)
    print(form.content)
    print(flask.request.method)

    if flask.request.method == 'POST':
        
        print(currentUser.id)
        
        post = libpost.Post(
            form.title.data,
            datetime.datetime.today(),
            form.content.data
        )
        print(post())
        
        db.insert_userPost(
            currentUser,
            post
        )
        print("yea")
            
    return flask.render_template('user_profile/profile.html', currentUser = currentUser, form = form)

@app.route("/logout.html")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)