# Generated by Django 3.2.7 on 2021-09-29 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SNS_App', '0003_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetmodel',
            name='title',
            field=models.CharField(max_length=70),
        ),
    ]
