# Generated by Django 3.2 on 2022-09-19 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
