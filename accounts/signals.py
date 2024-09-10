from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    This function listens for the post_save event on the User model. 
    If the User instance is newly created (created=True), it creates a corresponding Profile.
    """    
    if created:
        Profile.objects.create(user=instance)
        
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     """
#     This function ensures that the Profile is saved whenever the User is saved, 
#     in case any related updates need to be persisted.
#     """    
#     instance.profile.save()