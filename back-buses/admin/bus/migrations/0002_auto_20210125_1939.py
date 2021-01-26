# Generated by Django 3.1.5 on 2021-01-25 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chofer', '0003_auto_20210125_1939'),
        ('bus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='cantidad_asientos',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='bus',
            name='chofer_asignado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chofer.chofer'),
        ),
    ]