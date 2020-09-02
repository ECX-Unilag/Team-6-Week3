from django.db import models
from django.contrib.auth.models import User
from language.models import Language


User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True, default='default.jpg')
    GENDER_CHOICES = (
        ('Female', 'Female'),
        ('Male', 'Male'),
    )
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, default='Male')
    languages = models.ManyToManyField(Language, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.user.username} Profile'
