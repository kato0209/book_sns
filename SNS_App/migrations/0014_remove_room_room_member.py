# Generated by Django 3.2.7 on 2021-12-29 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SNS_App', '0013_alter_entries_joined_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='room_member',
        ),
    ]
