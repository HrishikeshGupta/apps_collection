# Generated by Django 3.0.7 on 2020-07-02 13:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('studentdb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_data',
            name='id',
        ),
        migrations.AddField(
            model_name='student_data',
            name='gender',
            field=models.CharField(default=datetime.datetime(2020, 7, 2, 13, 23, 4, 375012, tzinfo=utc), max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student_data',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False),
        ),
    ]
