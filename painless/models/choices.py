class PostStatus:
    """Check Published or Draft Status of a post
    
    Arguments:
        is_charfield {[bool]} -- check for charfield models or positiveintegerfield
    """

    def __init__(self, is_charfield = True):
               
        if is_charfield:
            self.DRAFT = 'd'
            self.PUBLISHED = 'p'
        else:
            self.DRAFT = 0
            self.PUBLISHED = 1
        
    
    def is_published(self, value):
        """[summary]
    
        Arguments:
            Postable {[str, int]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        return True if value == self.PUBLISHED else False
    
    def is_draft(self, value):
        return True if value == self.DRAFT else False
    
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
