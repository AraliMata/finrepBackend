# Generated by Django 4.0.2 on 2022-04-28 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinRepApp', '0011_rename_totalabonos_movimientos_abonos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientos',
            name='codigo',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='movimientos',
            name='nombre',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='movimientos',
            name='saldoInicial',
            field=models.FloatField(null=True),
        ),
    ]
