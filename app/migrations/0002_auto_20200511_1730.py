# Generated by Django 3.0.3 on 2020-05-11 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dropoff_point',
            field=models.TextField(blank=True, choices=[('Uniben', (('HALL4', 'Hall4'), ('HALL3', 'Hall3'), ('HALL2', 'Hall2'), ('HALL1', 'Hall1'), ('Main Gate', 'Main gate'), ('Green Park', 'Green Park'), ('GTBANK', 'GTBank Wifi Spot'), ('NAAS Garden', 'Naas Garden'), ('Physical Science Complex', 'Physical Science Complex'), ('Med Complex', 'Medical Science Complex'), ('Basement', 'Basement'), ('JUNE12', 'June12'), ('Engineering Park', 'Engineering Park')))], default='Main Gate', max_length=250),
        ),
    ]
