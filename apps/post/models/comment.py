from django.db import models
from django.conf import settings

class Comment(models.Model):
    person_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_id = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Content')

    def __str__(self):
        return self.content[:10] + '...'
