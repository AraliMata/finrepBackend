from sqlite3.dbapi2 import _AggregateProtocol
from django.shortcuts import render, redirect
from backendEmployeeTest.models import Employee
from .serializer import EmployeeSerializer
from rest_framework import viewsets


# Create your views here.
class Employee(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer 