from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# class comment(models.Model):
#     title = models.CharField(max_length=250 , min_length = 10 , null=False )
#     text = models.CharField(max_length=250 , min_length = 10 , null=False)
#     email = mode
# ls.CharField(max_length=250 , min_length = 10 , null=True) #valid email
from django.db.models import CASCADE
from django.utils.safestring import mark_safe


class Comment(models.Model):
    email = models.EmailField()
    subject = models.CharField(null=False, max_length=250)
    message = models.CharField(null=False, max_length=250)


class Person(models.Model):
    user = models.OneToOneField(to=User, on_delete=CASCADE)
    GENDER_TYPE = (("M", "MALE"), ("F", "FEMALE"),)
    gender = models.CharField(null=True, choices=GENDER_TYPE, max_length=1)
    bio = models.TextField(null=True)
    picture = models.FileField(blank=True, null=True, upload_to="static/food_pics/")

    def image_tag(self):
        return mark_safe("<img src='/%s' style='max-width:250px; "
                         "height=auto'/>" % self.picture)

