from django.conf import settings
from django.db import models
from django.utils.text import slugify
from accounts.models import BaseModel
from taggit.managers import TaggableManager

class Category(BaseModel, models.Model):
    name = models.CharField(max_length=150, unique=True)

    def get_category_posts(self):
        return Post.objects.filter(category=self)
    
    def get_all_category():
        return [
            {
                "id":category.id, 
                "name":category.name
            } for category in Category.objects.filter()
        ]
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'

class Post(BaseModel, models.Model):
    slug = models.SlugField(null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    postImage = models.CharField(max_length=255, null=True, blank=True)
    tags = TaggableManager()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    
    def save(self, *args, **kwargs):
        self.postImage = f'https://picsum.photos/680/320' 
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)
    
    def get_comments(self):
        return Comment.objects.filter(post=self)
    
    def get_likes(self):
        return Like.objects.filter(post=self)
    
    def __str__(self):
        return self.title

class Comment(BaseModel, models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=True, null=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, default=True, null=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'

class Like(BaseModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=True, null=True)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE, default=True, null=True)

    def __str__(self):
        return f'{self.user} liked {self.post}'