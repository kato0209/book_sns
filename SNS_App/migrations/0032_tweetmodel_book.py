# Generated by Django 3.2.7 on 2022-01-15 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SNS_App', '0031_auto_20220115_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetmodel',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SNS_App.bookdata', verbose_name='紐づく本'),
        ),
    ]
