# Generated by Django 3.1.7 on 2021-03-14 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_user_email_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='key',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
