class PostStatus:

    def __init__(self, is_charfield = True):
               
        if is_charfield:
            self.DRAFT = 'd'
            self.PUBLISHED = 'p'
        else:
            self.DRAFT = 0
            self.PUBLISHED = 1
 

    
    def get_draft(self):
        return self.DRAFT
    
    def get_publish(self):
        return self.PUBLISHED
    
    def get_status(self):
        status = (
            (self.DRAFT, 'Draft'),
            (self.PUBLISHED, 'Published'),
        )

        return status
