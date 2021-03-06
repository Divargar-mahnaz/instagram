# Generated by Django 3.1.7 on 2021-03-11 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(verbose_name='Content')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(blank=True, max_length=200, verbose_name='Location')),
                ('image', models.ImageField(upload_to='posts', verbose_name='Image')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
    ]
