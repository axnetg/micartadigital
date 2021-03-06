# Generated by Django 3.1.6 on 2021-04-01 23:34

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cartas', '0007_auto_20210311_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='plato',
            name='alergenos',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Gluten'), (2, 'Crustáceos'), (3, 'Huevos'), (4, 'Pescado'), (5, 'Cacahuetes'), (6, 'Soja'), (7, 'Lácteos'), (8, 'Frutos de cáscara'), (9, 'Apio'), (10, 'Mostaza'), (11, 'Granos de sésamo'), (12, 'Dióxido de azufre y sulfitos'), (13, 'Moluscos'), (14, 'Altramuces')], max_length=32),
        ),
    ]
