# Generated by Django 3.2.7 on 2022-01-14 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SNS_App', '0025_tweetmodel_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweetmodel',
            name='title',
        ),
    ]