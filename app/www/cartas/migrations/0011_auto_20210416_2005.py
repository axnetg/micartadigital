# Generated by Django 3.1.6 on 2021-04-16 18:05

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cartas', '0010_auto_20210408_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carta',
            options={'ordering': ['titulo']},
        ),
        migrations.AlterModelOptions(
            name='establecimiento',
            options={'ordering': ['nombre']},
        ),
        migrations.AlterModelOptions(
            name='plato',
            options={'ordering': ['orden']},
        ),
        migrations.AlterModelOptions(
            name='seccion',
            options={'ordering': ['orden']},
        ),
        migrations.AddField(
            model_name='carta',
            name='ultima_modificacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='plato',
            name='alergenos',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Altramuces'), (2, 'Apio'), (3, 'Cacahuetes'), (4, 'Crustáceos'), (5, 'Dióxido de azufre y sulfitos'), (6, 'Frutos de cáscara'), (7, 'Gluten'), (8, 'Granos de sésamo'), (9, 'Huevos'), (10, 'Lácteos'), (11, 'Moluscos'), (12, 'Mostaza'), (13, 'Pescado'), (14, 'Soja')], max_length=32),
        ),
    ]