# Generated by Django 3.2.7 on 2022-01-14 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SNS_App', '0022_auto_20220114_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetmodel',
            name='ISBNcode',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='tweetmodel',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='紐づくユーザー'),
        ),
    ]
