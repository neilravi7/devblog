import random
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from accounts.models import BaseModel

class Post(BaseModel, models.Model):
    slug = models.SlugField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    postImage = models.CharField(max_length=255)    

    
    def save(self, args, kwargs):
        num = random.randint(1, 15)
        self.slug = slugify()
        self.postImage = f'https://randomuser.me/api/portraits/men/{num}.jpg'
        return super().save(args, kwargs)

    def __str__(self):
        return self.title

class Comment(BaseModel, models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'

class Like(BaseModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} liked {self.post}'