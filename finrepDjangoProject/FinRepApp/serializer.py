from rest_framework import serializers
from .models import Cuentas

class CuentasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuentas
        fields = [
        'idEmpresa',
        'codigo',
        'nombre'
        ]

