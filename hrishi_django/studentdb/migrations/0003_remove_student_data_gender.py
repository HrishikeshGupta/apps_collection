# Generated by Django 3.0.7 on 2020-07-04 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentdb', '0002_auto_20200702_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_data',
            name='gender',
        ),
    ]
