# Generated by Django 4.0.2 on 2022-05-27 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FinRepApp', '0015_codigos_agrupadores_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario_empresa',
            name='idUsuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
