# Generated by Django 4.2.16 on 2024-09-28 04:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_alter_mynotes_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mynotes',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
