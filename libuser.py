from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, login, password = '', email = '', posts = []):
        self.id = login
        self.email = email
        self.login = login
        self.password = password
        self.posts = posts
    
    def __call__(self):
        return {
        #    "id": self.id,
            "Email": self.email,
            "Login": self.login,
            "Password": self.password,
            "Posts": self.posts
        }
