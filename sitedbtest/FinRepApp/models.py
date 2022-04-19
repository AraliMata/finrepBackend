from django.db import models
# import uuid
# unique_id = uuid.uuid4().hex

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    contrasena = models.CharField(max_length=100)

    class Meta:
        db_table = "usuario"

class Empresa(models.Model):
    # id = models.CharField(max_length=100,primary_key=True,
    #     default=unique_id, editable=False
    # )
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "empresa"

class Usuario_Empresa(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        db_table = "usuario_empresa"

class Cuentas(models.Model):
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "cuentas"

class Movimientos(models.Model):
    idCuenta = models.ForeignKey(Cuentas, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100)
    saldoInicial = models.FloatField()
    totalCargos = models.FloatField()
    totalAbonos = models.FloatField()
    saldoAcumulado = models.FloatField()
    fechaInicio = models.DateField()
    fechaFinal = models.DateField()

    class Meta:
        db_table = "movimientos"