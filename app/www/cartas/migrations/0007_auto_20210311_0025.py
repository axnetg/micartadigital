# Generated by Django 3.1.6 on 2021-03-10 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartas', '0006_plato_orden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plato',
            name='descripcion',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='plato',
            name='precio',
            field=models.FloatField(),
        ),
    ]