# Generated by Django 4.1.7 on 2023-03-23 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0003_alter_course_resource_alter_course_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=250)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sell.course')),
            ],
        ),
    ]