class User():
    def __init__(self, login, password, email = '', posts = []):
        self.email = email
        self.login = login
        self.password = password
        self.posts = posts
    
    def __call__(self):
        return {
            "Email": self.email,
            "Login": self.login,
            "Password": self.password,
            "Posts": self.posts
        }

