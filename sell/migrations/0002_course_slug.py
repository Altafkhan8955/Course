# Generated by Django 4.1.7 on 2023-03-17 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.CharField(default=' ', max_length=50),
            preserve_default=False,
        ),
    ]