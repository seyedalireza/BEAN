# Generated by Django 2.1.3 on 2018-11-23 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeanApp', '0004_auto_20181122_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='static/food_pics/'),
        ),
    ]
