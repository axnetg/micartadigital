# Generated by Django 3.1.6 on 2021-04-19 19:52

import cartas.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cartas', '0012_auto_20210419_2115'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carta',
            options={'ordering': ['titulo'], 'verbose_name': 'carta', 'verbose_name_plural': 'cartas'},
        ),
        migrations.AlterModelOptions(
            name='establecimiento',
            options={'ordering': ['nombre'], 'verbose_name': 'establecimiento', 'verbose_name_plural': 'establecimientos'},
        ),
        migrations.AlterModelOptions(
            name='plato',
            options={'ordering': ['orden'], 'verbose_name': 'plato', 'verbose_name_plural': 'platos'},
        ),
        migrations.AlterModelOptions(
            name='seccion',
            options={'ordering': ['orden'], 'verbose_name': 'sección', 'verbose_name_plural': 'secciones'},
        ),
        migrations.AlterField(
            model_name='carta',
            name='propietario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cartas', to=settings.AUTH_USER_MODEL, verbose_name='propietario'),
        ),
        migrations.AlterField(
            model_name='carta',
            name='titulo',
            field=models.CharField(max_length=100, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='carta',
            name='ultima_modificacion',
            field=models.DateTimeField(auto_now=True, verbose_name='última modificación'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='calle',
            field=models.CharField(max_length=200, verbose_name='calle'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='carta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='establecimientos', to='cartas.carta', verbose_name='carta'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='codigo_postal',
            field=models.CharField(max_length=5, verbose_name='código postal'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=cartas.models.get_file_path, verbose_name='imagen de portada'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='localidad',
            field=models.CharField(max_length=100, verbose_name='localidad'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='propietario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='establecimientos', to=settings.AUTH_USER_MODEL, verbose_name='propietario'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='provincia',
            field=models.CharField(max_length=50, verbose_name='provincia'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='dirección URL'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, verbose_name='teléfono'),
        ),
        migrations.AlterField(
            model_name='plato',
            name='alergenos',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Altramuces'), (2, 'Apio'), (3, 'Cacahuetes'), (4, 'Crustáceos'), (5, 'Dióxido de azufre y sulfitos'), (6, 'Frutos de cáscara'), (7, 'Gluten'), (8, 'Granos de sésamo'), (9, 'Huevos'), (10, 'Lácteos'), (11, 'Moluscos'), (12, 'Mostaza'), (13, 'Pescado'), (14, 'Soja')], max_length=32, verbose_name='alérgenos'),
        ),
        migrations.AlterField(
            model_name='plato',
            name='descripcion',
            field=models.CharField(blank=True, max_length=400, verbose_name='descripción'),
        ),
        migrations.AlterField(
            model_name='plato',
            name='orden',
            field=models.PositiveSmallIntegerField(verbose_name='orden'),
        ),
        migrations.AlterField(
            model_name='plato',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='precio'),
        ),
        migrations.AlterField(
            model_name='plato',
            name='seccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='platos', to='cartas.seccion', verbose_name='sección'),
        ),
        migrations.AlterField(
            model_name='plato',
            name='titulo',
            field=models.CharField(max_length=100, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='carta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secciones', to='cartas.carta', verbose_name='carta'),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='orden',
            field=models.PositiveSmallIntegerField(verbose_name='orden'),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='titulo',
            field=models.CharField(max_length=100, verbose_name='título'),
        ),
    ]
