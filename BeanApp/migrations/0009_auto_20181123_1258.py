# Generated by Django 2.1.3 on 2018-11-23 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeanApp', '0008_auto_20181123_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='static/food_pics/'),
        ),
    ]
