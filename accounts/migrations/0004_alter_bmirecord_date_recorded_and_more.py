# Generated by Django 5.0.7 on 2024-08-10 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_bmirecord_date_recorded_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bmirecord',
            name='date_recorded',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='savedexercise',
            name='date_executed',
            field=models.DateField(auto_now=True),
        ),
    ]
