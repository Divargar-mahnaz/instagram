# Generated by Django 3.1.7 on 2021-02-28 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20210226_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='default_profile.png', upload_to='posts', verbose_name='Image'),
        ),
    ]