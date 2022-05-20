from rest_framework import serializers
from .models import Cuentas, Usuario, Empresa, Usuario_Empresa
from .models import Cuentas
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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
class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
