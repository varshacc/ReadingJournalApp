from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    RATING_RANGE = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    article = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    startDate = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True,null=True)
    endDate = models.DateTimeField(auto_now_add=False,auto_now=False, blank=True,null=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.IntegerField(choices=RATING_RANGE)
    thoughts = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.article

    class Meta:
        order_with_respect_to = 'user'
