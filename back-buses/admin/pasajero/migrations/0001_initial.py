# Generated by Django 3.1.5 on 2021-01-28 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pasajero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('run', models.CharField(max_length=10)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Pasajeros',
            },
        ),
    ]
