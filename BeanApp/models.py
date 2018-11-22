from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# class comment(models.Model):
#     title = models.CharField(max_length=250 , min_length = 10 , null=False )
#     text = models.CharField(max_length=250 , min_length = 10 , null=False)
#     email = mode
# ls.CharField(max_length=250 , min_length = 10 , null=True) #valid email
from django.db.models import CASCADE
from reportlab.platypus.doctemplate import onDrawStr


class Comment(models.Model):
    email = models.EmailField()
    subject = models.CharField(null=False, max_length=250)
    message = models.CharField(null=False, max_length=250)


class Person(models.Model):
    user = models.ForeignKey(to=User, on_delete=CASCADE)
    GENDER_TYPE = (("M", "MALE"), ("F", "FEMALE"))
    gender = models.IntegerField(choices=GENDER_TYPE)
    bio = models.TextField()
