# Generated by Django 3.1.7 on 2021-03-04 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20210304_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='follow',
            new_name='following',
        ),
    ]