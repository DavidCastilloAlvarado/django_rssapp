from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.


class log_errors(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    id_feed = models.IntegerField()
    url = models.CharField(max_length=200)

    class Meta:
        ordering = ['-created_on']
        db_table = 'log_error'

    def __str__(self):
        return self.url


class User_feed(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)  # , db_index=True,
    author = models.CharField(max_length=200,
                              db_index=True,
                              blank=False,
                              null=False)
    title = models.CharField(max_length=200)
    body = models.CharField(blank=True, max_length=200)
    url = models.URLField(blank=False, null=False, max_length=200)

    class Meta:
        ordering = ['-created_on']
        db_table = 'user_feeds'

    def __str__(self):
        return self.title
