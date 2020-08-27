from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='media/avatar', blank=True)
    objects = models.Manager()

class Language(models.Model):
    name = models.CharField(_('Name'), max_length=20)
    brief_description = models.CharField(_('Brief Description'), max_length=300, blank=True)
    objects = models.Manager()
    def __str__(self):
        return self.name

class Stage(models.Model):
    NUMBER = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),
        ('9','9'),
        ('10','10'),
    )
    
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    number = models.CharField(_('Number'), max_length=2, choices=NUMBER)
    objects = models.Manager()
    def __str__(self):
        return self.number

class StudyMaterial(models.Model):
    stage = models.OneToOneField(Stage, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    topic = models.CharField(_('Topic'), max_length=30)
    text = models.TextField(_('Topic Details'))
    audio = models.FileField(upload_to='media/audio', blank=True)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.topic
"""
class Quiz(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)"""

class Question(models.Model):
    #language = models.ForeignKey(Language, on_delete=models.CASCADE)
    #stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    text = models.CharField(_('Question'), max_length=100)
    objects = models.Manager()
    def __str__(self):
        return self.text

class AnswerOptions(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    options_text = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    objects = models.Manager()
    def __str__(self):
        return self.options_text

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField(_('Score'), default=0 )
    objects = models.Manager()