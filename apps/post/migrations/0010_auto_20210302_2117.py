# Generated by Django 3.1.7 on 2021-03-02 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20210301_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='posts', verbose_name='Image'),
        ),
    ]