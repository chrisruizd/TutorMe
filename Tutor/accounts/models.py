from cProfile import label
from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django import forms
from PIL import Image

CHOICES = (
    ('student', 'STUDENT'),
    ('tutor', 'TUTOR'),   
)


class Profile(models.Model):
    #one user can have one profile and one profile can have one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    bio = models.TextField(blank = True)
    account_Type = models.CharField(max_length=10, choices=CHOICES, default='none')
    github = models.CharField(max_length=200, null=True, blank=True, default='none')
    twitter = models.CharField(max_length=200, null=True, blank=True, default='none')
    linkedin = models.CharField(max_length=200, null=True, blank=True, default='none')
    facebook = models.CharField(max_length=200, null=True, blank=True, default='none')
    instagram = models.CharField(max_length=200, null=True, blank=True, default='none')

    followed = models.ManyToManyField(User, related_name='followed', default=None, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kawargs):
        super().save(*args, **kawargs)

        img = Image.open(self.image.path)   #getting image

        #resize image if grater than 300px
        if img.height > 300 or img.width >300:
            im_size = (300, 300)
            img.thumbnail(im_size)
            img.save(self.image.path)


    @property
    def num_follow(self):
        return self.followed.all().count()



CHOICES = (
    ('Follow', 'Follow'),
    ('Unfollow', 'Unfollow')
) 

class FollowersCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.CharField(choices=CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.user)