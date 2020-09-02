from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils import timezone


class LanguageQuerySet(models.QuerySet):

    def search(self, query):
        lookup = (
            Q(name__icontains=query)
        )
        return self.filter(lookup)


class LanguageManager(models.Manager):
    def get_queryset(self):
        return LanguageQuerySet(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class Language(models.Model):
    name = models.CharField(_('Name'), max_length=20, unique=True)
    brief_description = models.CharField(_('Brief Description'), max_length=300, blank=True)
    objects = LanguageManager()

    def __str__(self):
        return self.name


all_languages = Language.objects.all()


class Stage(models.Model):
    NUMBER = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )

    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    number = models.CharField(_('Number'), max_length=2, choices=NUMBER)
    name = models.CharField(_('Name'), max_length=40)
    objects = models.Manager()

    class Meta:
        unique_together = (("language", "number"),)

    def __str__(self):
        return f'{self.name} ({self.language.name})'


class StudyMaterial(models.Model):
    stage = models.OneToOneField(Stage, on_delete=models.CASCADE)
    # language = models.ForeignKey(Language, on_delete=models.CASCADE)
    topic = models.CharField(_('Topic'), max_length=30)
    text = models.TextField(_('Topic Details'))
    audio = models.FileField(upload_to='audio', blank=True)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.topic} for {self.stage.language.name}'


class Question(models.Model):
    # language = models.ForeignKey(Language, on_delete=models.CASCADE)
    # stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    text = models.CharField(_('Question'), max_length=100)
    audio = models.FileField(upload_to='audio', blank=True, null=True)
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
    study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    score = models.IntegerField(_('Score'), default=0)
    objects = models.Manager()
    # answer = models.


# class Progress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     languages = models.ForeignKey(Language, on_delete=models.CASCADE)
#     progress = models.IntegerField(default=0, validators=[
#             MaxValueValidator(100),
#             MinValueValidator(0)
#         ])
#     objects = models.Manager()


class SearchQuery(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    query = models.CharField(max_length=220)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query

