from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as gl

class BaseModel(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.
class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("email required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is staff user')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser flag is false')
        
        return self._create_user(email, password, **extra_fields)

class User(BaseModel, AbstractUser, PermissionsMixin):
    username = None
    
    email = models.EmailField(gl('email address'), unique=True)

    objects = UserProfileManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'accounts'
    
    def __str__(self):
        return self.email
    
    def __unicode__(self):
        return self.id
    
    def get_profile(self):
        instance = User.objects.get(id=self.id);
        
        following = [
            {
                "id":following.user.id, 
                "name":f'{following.user.first_name} {following.user.last_name}'
            } for following in instance.following.all()
        ]

        followers = [
            {
                "id":follower.user.id, 
                "name":f'{follower.user.first_name} {follower.user.last_name}'
            } for follower in instance.followers.all()
        ]
        return {
            "user_id":str(self.id),
            "email":self.email,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "bio":self.profile.bio,
            "profile_image":self.profile.profile_image,
            "following":following,
            "followers":followers,
        }
    
    # def get_user_post(self){
    #     self.
    # }
    
    
class Profile(BaseModel, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=500, null=True, blank=True)
    profile_image = models.URLField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)    

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def save(self, *args, **kwargs):
        self.profile_image = 'https://placebeard.it/520x520'
        return super(Profile, self).save(*args, **kwargs)


class Followers(BaseModel, models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        db_table = 'followers'
        unique_together = ('user', 'follower')

    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"

