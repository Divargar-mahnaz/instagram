# Generated by Django 3.1.7 on 2021-03-04 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_auto_20210302_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(blank=True, to='user.User', verbose_name='follow'),
        ),
    ]