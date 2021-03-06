# Generated by Django 3.1.6 on 2021-03-10 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cartas', '0004_auto_20210224_0038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('orden', models.PositiveSmallIntegerField()),
                ('carta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secciones', to='cartas.carta')),
            ],
        ),
        migrations.CreateModel(
            name='Plato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=400)),
                ('precio', models.PositiveIntegerField()),
                ('seccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='platos', to='cartas.seccion')),
            ],
        ),
    ]
