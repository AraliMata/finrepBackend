# Generated by Django 4.0.2 on 2022-04-28 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FinRepApp', '0007_rename_fechafinal_movimientos_fecha_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimientos',
            name='saldoAcumulado',
        ),
    ]
