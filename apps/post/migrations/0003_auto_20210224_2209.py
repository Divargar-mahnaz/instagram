# Generated by Django 3.1.7 on 2021-02-24 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_user_slug'),
        ('post', '0002_auto_20210224_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, to='user.User', verbose_name='Like'),
        ),
    ]