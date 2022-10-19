class Comment():

    # Class Initializer, takes 5 parameters
    def __init__(self, id, author_id, post_id, content):
        self.id = id
        self.author_id = author_id
        self.post_id = post_id
        self.content = content
        self.author = None
        self.post = None