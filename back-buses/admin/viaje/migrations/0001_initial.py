# Generated by Django 3.1.5 on 2021-01-25 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trayecto', '0001_initial'),
        ('pasajero', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('pasajero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pasajero.pasajero')),
                ('trayecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trayecto.trayecto')),
            ],
        ),
    ]