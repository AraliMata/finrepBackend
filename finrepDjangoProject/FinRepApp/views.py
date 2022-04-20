from django.shortcuts import render, redirect
from FinRepApp.models import Cuentas
from .serializer import CuentasSerializer
from rest_framework import viewsets


# Create your views here.
class Cuentas(viewsets.ModelViewSet):
    queryset = Cuentas.objects.all()
    serializer_class = CuentasSerializer