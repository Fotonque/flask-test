import pymongo
import libuser
import libpost

#Cluster0 = ""
#db_password = "BxCKoHUuMc4y2meB"

#try:
#    Cluster0 = pymongo.MongoClient("mongodb://Fotonque:BxCKoHUuMc4y2meB@fotondb-shard-00-00.jxjyx.mongodb.net:27017,fotondb-shard-00-01.jxjyx.mongodb.net:27017,fotondb-shard-00-02.jxjyx.mongodb.net:27017/flask_db?ssl=true&replicaSet=FotonDB-shard-0&authSource=admin&retryWrites=true&w=majority")
#    print("Cluster connection: success")
#except:
#    print("Cluster connection: error occurred")

#db = Cluster0.admin
#serverStatusResult=db.command("serverStatus")
#print(serverStatusResult)

#db = Cluster0.flask_db

#result = db.Users.insert_one({
#    'username': "somename",
#    'password': "pass",
#    'email': "email"
#})


#user = User(userName_entry.get(), self.password_entry.get())
#userFromDB = db.Users.find_one(user())

#print(userFromDB)


class Database():
    SUCCESS = "SUCCESS"
    ERROR_USER_EXIST = "ERROR_USER_EXIST"
    def __init__(self, cluster):
        """
        cluster - cluster connection string
        """
        self.cluster = cluster
        self.db = cluster.flask_db

    def insert_user(self, user):
        """
        user - class User to insert
        """
        print(self.find_user(user))
        if self.find_user(user) == None:
            self.db.Users.insert_one({
                "Email": user()["Email"],
                'Login': user()['Login'],
                'Password': user()['Password']
            })
            return self.SUCCESS
        else:
            return self.ERROR_USER_EXIST

    def insert_userPost(self, user, post):
        """
        user - class User to insert
        post - class Post to insert
        """
        self.db.Posts.insert_one({
            'Login': user()['Login'],
            "title": post()['title'],
            "date": post()['date'],
            "content": post()['content'],
        })
        return SUCCESS

    def find_user(self, user):
        db_user = self.db.Users.find_one({
            'Login': user()['Login']
        })
        
        if db_user != None:
            user.email = db_user['Email']
            posts = self.find_userPosts(user)
            user.posts = posts
        else:
            return None

        return user

    def find_userPosts(self, user):
        """
        Returns array of class Post
        """
        postsArr = []
        posts = self.db.Posts.find({
            'Login': user()['Login']
        })
        for upost in posts:
            postsArr.append(
                libpost.Post(
                    upost['title'],
                    upost['date'],
                    upost['content']
            ))
        return posts

#db = Database(Cluster0)
#testUser = libuser.User('log', 'pas')
#testPost = libpost.Post('title', 'date', 'somecontent')
#result = db.find_user(testUser)
#res = db.insert_user(testUser)
#print(res)
#db.insert_userPost(testUser, testPost)