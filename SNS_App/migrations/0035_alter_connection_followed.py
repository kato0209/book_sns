# Generated by Django 3.2.7 on 2022-05-16 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SNS_App', '0034_auto_20220516_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='followed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed', to=settings.AUTH_USER_MODEL),
        ),
    ]
