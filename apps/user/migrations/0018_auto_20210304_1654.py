# Generated by Django 3.1.7 on 2021-03-04 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20210304_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(blank=True, related_name='followers', to='user.User', verbose_name='follow'),
        ),
    ]