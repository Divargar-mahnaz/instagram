# Generated by Django 3.1.7 on 2021-03-12 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_email_confirmed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_confirmed',
        ),
    ]
