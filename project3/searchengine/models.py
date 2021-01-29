from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

def get_image_path(instance, filename):
    return os.path.join('users', str(instance.id), filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    favorite_games = models.TextField(blank=True, help_text='Add games by seperating with a "|" character')
    favorite_streamers = models.TextField(blank=True, help_text='Add streamers by seperating with a "|" character')
    # favorite_streamers = models.CharField(blank=True, max_length = 1024)

    streamer0 = models.CharField(blank = True, max_length = 255)
    streamer1 = models.CharField(blank = True, max_length = 255)
    streamer2 = models.CharField(blank = True, max_length = 255)
    streamer3 = models.CharField(blank = True, max_length = 255)
    streamer4 = models.CharField(blank = True, max_length = 255)
    streamer5 = models.CharField(blank = True, max_length = 255)
    streamer6 = models.CharField(blank = True, max_length = 255)
    streamer7 = models.CharField(blank = True, max_length = 255)
    streamer8 = models.CharField(blank = True, max_length = 255)
    streamer9 = models.CharField(blank = True, max_length = 255)

    game0 =  models.CharField(blank = True, max_length = 255)
    game1 =  models.CharField(blank = True, max_length = 255)
    game2 =  models.CharField(blank = True, max_length = 255)
    game3 =  models.CharField(blank = True, max_length = 255)
    game4 =  models.CharField(blank = True, max_length = 255)
    game5 =  models.CharField(blank = True, max_length = 255)
    game6 =  models.CharField(blank = True, max_length = 255)
    game7 =  models.CharField(blank = True, max_length = 255)
    game8 =  models.CharField(blank = True, max_length = 255)
    game9 =  models.CharField(blank = True, max_length = 255)

    bio = models.TextField(blank=True)
    # signup_confirmation = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # Streamers.objects.create(user=instance)
    instance.profile.save()
    # instance.streamers.save()
