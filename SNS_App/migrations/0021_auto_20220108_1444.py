# Generated by Django 3.2.7 on 2022-01-08 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SNS_App', '0020_tweetmodel_isbncode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetmodel',
            name='ISBNcode',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='tweetmodel',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='tweetmodel',
            name='rating',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='tweetmodel',
            name='title',
            field=models.CharField(blank=True, max_length=70),
        ),
    ]