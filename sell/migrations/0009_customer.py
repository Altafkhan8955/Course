# Generated by Django 4.1.7 on 2023-04-03 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0008_couponcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=250)),
            ],
        ),
    ]
