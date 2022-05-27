from operator import truediv
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    contrasena = models.CharField(max_length=100)

    class Meta:
        db_table = "usuario"

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "empresa"

class Usuario_Empresa(models.Model):
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    idEmpresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)

    class Meta:
        db_table = "usuario_empresa"

class Cuentas(models.Model):
    idEmpresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "cuentas"

class Movimientos(models.Model):
    idEmpresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100,null=True)
    nombre = models.CharField(max_length=100,null=True)
    codigoAgrupador = models.CharField(max_length=100,null=True)
    nombreAgrupador = models.CharField(max_length=100,null=True)
    concepto = models.CharField(max_length=100, null=True)
    referencia = models.CharField(max_length=100, null=True)
    ingresoEgreso = models.CharField(max_length=100,null=True)
    tipo = models.CharField(max_length=100,null=True)
    saldoInicial = models.FloatField(null=True)
    cargos = models.FloatField(null=True)
    abonos = models.FloatField(null=True)
    # saldoAcumulado = models.FloatField()
    fecha = models.DateField(null=True)

    class Meta:
        db_table = "movimientos"

class Codigos_Agrupadores(models.Model):
    idEmpresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

    class Meta:
        db_table = "codigos_agrupadores"