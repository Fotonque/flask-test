class Post:
    def __init__(self, title, date, content):
        self.title = title
        self.date = date
        self.content = content

    def __call__(self):
        return {
            "title": self.title,
            "date": self.date,
            "content": self.content,
        }