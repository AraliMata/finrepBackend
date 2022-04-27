# Generated by Django 4.0.2 on 2022-04-27 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FinRepApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimientos',
            name='idCuenta',
        ),
        migrations.AddField(
            model_name='movimientos',
            name='idEmpresa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='FinRepApp.empresa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movimientos',
            name='nombre',
            field=models.CharField(default='nombre', max_length=100),
            preserve_default=False,
        ),
    ]
