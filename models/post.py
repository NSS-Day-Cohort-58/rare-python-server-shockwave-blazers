class Post():

    # Class Initializer, takes 11 parameters
    def __init__(self, id, user_id, category_id, title, publication_date, image_url, content, approved):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.title = title
        self.publication_date = publication_date
        self.image_url = image_url
        self.content = content
        self.approved = approved
        self.user = None
        self.category = None
        self.tag = None
        self.reaction = None