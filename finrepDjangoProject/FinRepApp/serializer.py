from rest_framework import serializers
from .models import Cuentas, Usuario, Empresa, Usuario_Empresa

class CuentasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuentas
        fields = [
        'idEmpresa',
        'codigo',
        'nombre'
        ]

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
        'nombre',
        'correo',
        'contrasena'
        ]

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = [
        'nombre'
        ]
class Usuario_EmpresaAuxSerializer(serializers.Serializer):
    idEmpresa = EmpresaSerializer()
    idUsuario = UsuarioSerializer()

class Usuario_EmpresaSerializer(serializers.Serializer):
    Usuario_Empresa = Usuario_EmpresaAuxSerializer()
    # class Meta:
    #     model = Usuario_Empresa
    #     fields = [
    #     'idUsuario_id',
    #     'idEmpresa_id',
    #     ]
