"""finrepDjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from email.mime import base
from django.contrib import admin
from django.urls import include, path
from numpy import fix
from backendEmployeeTest.views import Employee
from FinRepApp import views
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.static import serve
import os
import pandas as pd
from calendar import month_name
from datetime import datetime
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime 
from datetime import datetime
import pyodbc
import json as js


# cuentas_list = views.Cuentas.as_view({
#     'get': 'list'
# })


global catalogo
catalogo = pd.read_excel('catalogo.xlsx')

router = routers.DefaultRouter(trailing_slash=False)
router.register('employeedetails', Employee)
router.register('cuentas', views.Cuentas)
# router.register('cuentas', cuentas_list, basename='cuentas-list')
# recibirArchivoPost = views.recibirArchivo.as_view({'post': 'create'})
# router.register('xlsx', recibirArchivoPost)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLUTTER_WEB_APP = os.path.join(BASE_DIR, 'flutter_web_app')

def flutter_redirect(request, resource):
    return serve(request, resource, FLUTTER_WEB_APP)

def acomodarResponse(movimientos):
    activos = {'circulante':[['', '']], 'fijo': [['', '']], 'diferido':[['', '']]}
    pasivos = {'circulante':[['', '']], 'fijo': [['', '']], 'diferido':[['', '']]}
    capital = {'capital': [['', '']]}

    sumasActivo = [0,0,0,0]
    sumasPasivo = [0,0,0,0]
    sumasCapital = [0,0,0]

    #6
    for movimiento in movimientos:
        if movimiento[2] != 0.0 and movimiento[1] != 'Otros':
            if movimiento[0][0] == '1':
                par = [movimiento[1], movimiento[2]]
                if movimiento[0][1] == '0':
                    activos['circulante'].append(par)
                    sumasActivo[0] += movimiento[2]
                elif movimiento[0][1] == '2':
                    if movimiento[0][2] == '1':
                        par = [movimiento[1], -(movimiento[2])]
                        activos['fijo'].append(par)
                        sumasActivo[1] += par[1]
                    else:
                        activos['fijo'].append(par)
                        sumasActivo[1] += par[1]
                elif movimiento[0][1] == '4': 
                    activos['diferido'].append(par)
                    sumasActivo[2] += movimiento[2]
            elif movimiento[0][0] == '2':
                if movimiento[5] < 0:
                    par = [movimiento[1], movimiento[4]]
                else:
                    par = [movimiento[1], movimiento[3]]

                if movimiento[0][1] == '0':
                    pasivos['circulante'].append(par)
                    # sumasPasivo[0] += movimiento[2]
                    sumasPasivo[0] += par[1]
                elif movimiento[0][1] == '2': 
                    pasivos['fijo'].append(par)
                    # sumasPasivo[1] += movimiento[2]
                    sumasPasivo[0] += par[1]
                elif movimiento[0][1] == '4': 
                    pasivos['diferido'].append(par)
                    # sumasPasivo[2] += movimiento[2]
                    sumasPasivo[0] += par[1]
            else:
                par = [movimiento[1], movimiento[2]]
                capital['capital'].append(par)
                sumasCapital[0] += movimiento[2]

    sumasActivo[3] = sum(sumasActivo[0:3])
    sumasPasivo[3] = sum(sumasPasivo[0:3])
    sumasCapital[1] = sumasCapital[0] + 115631.77
    sumasCapital[2] = sumasPasivo[3] + sumasCapital[1]

    activos['circulante'].append(['Total CIRCULANTE', sumasActivo[0]])
    activos['fijo'].append(['Total FIJO', sumasActivo[1]])
    activos['diferido'].append(['Total DIFERIDO', sumasActivo[2]])
    activos['diferido'].append(['SUMA DEL ACTIVO', sumasActivo[3]])

    pasivos['circulante'].append(['Total CIRCULANTE', sumasPasivo[0]])
    pasivos['fijo'].append(['Total FIJO', sumasPasivo[1]])
    pasivos['diferido'].append(['Total DIFERIDO', sumasPasivo[2]])
    pasivos['diferido'].append(['SUMA DEL PASIVO', sumasPasivo[3]])

    # capital['capital'].append(['Total CAPITAL', sumasCapital[0]])
    capital['capital'].append(['Total CAPITAL', sumasCapital[0]])
    capital['capital'].append(['Utilidad o Pérdida del Ejercicio', 115631.77])
    capital['capital'].append(['SUMA DEL CAPITAL', sumasCapital[1]])
    capital['capital'].append(['SUMA DEL PASIVO Y CAPITAL', sumasCapital[2]])
    
    balanceGeneral = {'activo': activos, 'pasivo': pasivos, 'capital':capital}
    print(balanceGeneral)
    return balanceGeneral

@api_view(['GET'])
def getMovimientos(request):
    init_db()
    dictionary ={ 
    "id": "04", 
    "name": "sunil", 
    "department": "HR"
    } 
    balanceGeneral = acomodarResponse(movimientoshacker())
    # Serializing json  
    json_object = js.dumps(balanceGeneral) 
    print(json_object)

    #print(json, "JSON")
    # return Response({"Valor de linea 0 columna 0":df_listo.iat[0,0]})
    return Response(json_object)                


def movimientoshacker():
    cursor = init_db()
    print("HOLA MAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #json = cursor.execute("SELECT * FROM [dbo].[movimientos]").fetchall()
    # json = cursor.execute("SELECT min([dbo].[movimientos].codigo) as codigo, CASE WHEN [dbo].[movimientos].codigo LIKE '102%' THEN 'Bancos' WHEN [dbo].[movimientos].codigo LIKE '101%' THEN 'Caja' WHEN [dbo].[movimientos].codigo LIKE '100%' THEN 'Fondo Fijo Caja' WHEN [dbo].[movimientos].codigo LIKE '103%' THEN 'Clientes' WHEN [dbo].[movimientos].codigo LIKE '104%' THEN 'Documentos por Cobrar' WHEN [dbo].[movimientos].codigo LIKE '105%' THEN 'Deudores Diversos' WHEN [dbo].[movimientos].codigo LIKE '106%' THEN 'IVA Acreditable' WHEN [dbo].[movimientos].codigo LIKE '107%' THEN 'Funcionarios y Empleados' WHEN [dbo].[movimientos].codigo LIKE '108%' THEN 'Inventarios' WHEN [dbo].[movimientos].codigo LIKE '109%' THEN 'Anticipo a Proveedores' WHEN [dbo].[movimientos].codigo LIKE '120%' THEN 'Mobiliario y Equipo de oficina' WHEN [dbo].[movimientos].codigo LIKE '121%' THEN 'Depreciación Acumulada de Mob y Eq. oficina' WHEN [dbo].[movimientos].codigo LIKE '122%' THEN 'Equipo de Transporte' WHEN [dbo].[movimientos].codigo LIKE '123%' THEN 'Depreciación Acumulada Equipo Transporte' WHEN [dbo].[movimientos].codigo LIKE '124%' THEN 'Equipo de cómputo' WHEN [dbo].[movimientos].codigo LIKE '125%' THEN 'Depreciación acumulada Eq. cómputo' WHEN [dbo].[movimientos].codigo LIKE '126%' THEN 'Edificios' WHEN [dbo].[movimientos].codigo LIKE '127%' THEN 'Depreciación Acumulada Edificios' WHEN [dbo].[movimientos].codigo LIKE '128%' THEN 'Terrenos' WHEN [dbo].[movimientos].codigo LIKE '129%' THEN 'Equipo de Servicios' WHEN [dbo].[movimientos].codigo LIKE '130%' THEN 'Depreciación acumulada de Eq. de Servicios' WHEN [dbo].[movimientos].codigo LIKE '140%' THEN 'Gastos de Organización' WHEN [dbo].[movimientos].codigo LIKE '141%' THEN 'Gastos de Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '142%' THEN 'Impuestos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '143%' THEN 'Gastos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '144%' THEN 'Deposito en Garantia' WHEN [dbo].[movimientos].codigo LIKE '150%' THEN 'Amortización Gastos Organización' WHEN [dbo].[movimientos].codigo LIKE '151%' THEN 'Amortización Gastos Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '200%' THEN 'PROVEEDORES' WHEN [dbo].[movimientos].codigo LIKE '201%' THEN 'ACREEDORES DIVERSOS' WHEN [dbo].[movimientos].codigo LIKE '202%' THEN 'IMPUESTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '203%' THEN 'DOCUMENTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '204%' THEN 'IVA Trasladado' WHEN [dbo].[movimientos].codigo LIKE '205%' THEN 'Anticipos de Clientes' WHEN [dbo].[movimientos].codigo LIKE '206%' THEN 'Sueldos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '207%' THEN 'Gastos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '208%' THEN 'PTU por Pagar' WHEN [dbo].[movimientos].codigo LIKE '220%' THEN 'Acreedores Hipotecarios' WHEN [dbo].[movimientos].codigo LIKE '221%' THEN 'Creditos Bancarios' WHEN [dbo].[movimientos].codigo LIKE '230%' THEN 'Intereses cobrados por adelantado' WHEN [dbo].[movimientos].codigo LIKE '000-030%' THEN 'CAPITAL' WHEN [dbo].[movimientos].codigo LIKE '000-031%' THEN 'Capital Social' WHEN [dbo].[movimientos].codigo LIKE '000-033%' THEN 'Resultado Ejercicios Anteriores' WHEN [dbo].[movimientos].codigo LIKE '000-034%' THEN 'Resultado del Ejercicio' WHEN [dbo].[movimientos].codigo LIKE '000-035%' THEN 'Utilidades Retenidas' ELSE 'Otros' END AS nombre, max([dbo].[movimientos].saldoInicial) - (SUM([dbo].[movimientos].abonos) - SUM([dbo].[movimientos].cargos)) as saldoAcumulado FROM [dbo].[movimientos] WHERE idEmpresa_id = 3  GROUP BY  CASE WHEN [dbo].[movimientos].codigo LIKE '102%' THEN 'Bancos' WHEN [dbo].[movimientos].codigo LIKE '101%' THEN 'Caja' WHEN [dbo].[movimientos].codigo LIKE '100%' THEN 'Fondo Fijo Caja' WHEN [dbo].[movimientos].codigo LIKE '103%' THEN 'Clientes' WHEN [dbo].[movimientos].codigo LIKE '104%' THEN 'Documentos por Cobrar' WHEN [dbo].[movimientos].codigo LIKE '105%' THEN 'Deudores Diversos' WHEN [dbo].[movimientos].codigo LIKE '106%' THEN 'IVA Acreditable' WHEN [dbo].[movimientos].codigo LIKE '107%' THEN 'Funcionarios y Empleados' WHEN [dbo].[movimientos].codigo LIKE '108%' THEN 'Inventarios' WHEN [dbo].[movimientos].codigo LIKE '109%' THEN 'Anticipo a Proveedores' WHEN [dbo].[movimientos].codigo LIKE '120%' THEN 'Mobiliario y Equipo de oficina' WHEN [dbo].[movimientos].codigo LIKE '121%' THEN 'Depreciación Acumulada de Mob y Eq. oficina' WHEN [dbo].[movimientos].codigo LIKE '122%' THEN 'Equipo de Transporte' WHEN [dbo].[movimientos].codigo LIKE '123%' THEN 'Depreciación Acumulada Equipo Transporte' WHEN [dbo].[movimientos].codigo LIKE '124%' THEN 'Equipo de cómputo' WHEN [dbo].[movimientos].codigo LIKE '125%' THEN 'Depreciación acumulada Eq. cómputo' WHEN [dbo].[movimientos].codigo LIKE '126%' THEN 'Edificios' WHEN [dbo].[movimientos].codigo LIKE '127%' THEN 'Depreciación Acumulada Edificios' WHEN [dbo].[movimientos].codigo LIKE '128%' THEN 'Terrenos' WHEN [dbo].[movimientos].codigo LIKE '129%' THEN 'Equipo de Servicios' WHEN [dbo].[movimientos].codigo LIKE '130%' THEN 'Depreciación acumulada de Eq. de Servicios' WHEN [dbo].[movimientos].codigo LIKE '140%' THEN 'Gastos de Organización' WHEN [dbo].[movimientos].codigo LIKE '141%' THEN 'Gastos de Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '142%' THEN 'Impuestos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '143%' THEN 'Gastos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '144%' THEN 'Deposito en Garantia' WHEN [dbo].[movimientos].codigo LIKE '150%' THEN 'Amortización Gastos Organización' WHEN [dbo].[movimientos].codigo LIKE '151%' THEN 'Amortización Gastos Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '200%' THEN 'PROVEEDORES' WHEN [dbo].[movimientos].codigo LIKE '201%' THEN 'ACREEDORES DIVERSOS' WHEN [dbo].[movimientos].codigo LIKE '202%' THEN 'IMPUESTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '203%' THEN 'DOCUMENTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '204%' THEN 'IVA Trasladado' WHEN [dbo].[movimientos].codigo LIKE '205%' THEN 'Anticipos de Clientes' WHEN [dbo].[movimientos].codigo LIKE '206%' THEN 'Sueldos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '207%' THEN 'Gastos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '208%' THEN 'PTU por Pagar' WHEN [dbo].[movimientos].codigo LIKE '220%' THEN 'Acreedores Hipotecarios' WHEN [dbo].[movimientos].codigo LIKE '221%' THEN 'Creditos Bancarios' WHEN [dbo].[movimientos].codigo LIKE '230%' THEN 'Intereses cobrados por adelantado' WHEN [dbo].[movimientos].codigo LIKE '000-030%' THEN 'CAPITAL' WHEN [dbo].[movimientos].codigo LIKE '000-031%' THEN 'Capital Social' WHEN [dbo].[movimientos].codigo LIKE '000-033%' THEN 'Resultado Ejercicios Anteriores' WHEN [dbo].[movimientos].codigo LIKE '000-034%' THEN 'Resultado del Ejercicio' WHEN [dbo].[movimientos].codigo LIKE '000-035%' THEN 'Utilidades Retenidas' ELSE 'Otros' END").fetchall()
    json = cursor.execute("SELECT min([dbo].[movimientos].codigo) as codigo, CASE WHEN [dbo].[movimientos].codigo LIKE '102%' THEN 'Bancos' WHEN [dbo].[movimientos].codigo LIKE '101%' THEN 'Caja' WHEN [dbo].[movimientos].codigo LIKE '100%' THEN 'Fondo Fijo Caja' WHEN [dbo].[movimientos].codigo LIKE '103%' THEN 'Clientes' WHEN [dbo].[movimientos].codigo LIKE '104%' THEN 'Documentos por Cobrar' WHEN [dbo].[movimientos].codigo LIKE '105%' THEN 'Deudores Diversos' WHEN [dbo].[movimientos].codigo LIKE '106%' THEN 'IVA Acreditable' WHEN [dbo].[movimientos].codigo LIKE '107%' THEN 'Funcionarios y Empleados' WHEN [dbo].[movimientos].codigo LIKE '108%' THEN 'Inventarios' WHEN [dbo].[movimientos].codigo LIKE '109%' THEN 'Anticipo a Proveedores' WHEN [dbo].[movimientos].codigo LIKE '120%' THEN 'Mobiliario y Equipo de oficina' WHEN [dbo].[movimientos].codigo LIKE '121%' THEN 'Depreciación Acumulada de Mob y Eq. oficina' WHEN [dbo].[movimientos].codigo LIKE '122%' THEN 'Equipo de Transporte' WHEN [dbo].[movimientos].codigo LIKE '123%' THEN 'Depreciación Acumulada Equipo Transporte' WHEN [dbo].[movimientos].codigo LIKE '124%' THEN 'Equipo de cómputo' WHEN [dbo].[movimientos].codigo LIKE '125%' THEN 'Depreciación acumulada Eq. cómputo' WHEN [dbo].[movimientos].codigo LIKE '126%' THEN 'Edificios' WHEN [dbo].[movimientos].codigo LIKE '127%' THEN 'Depreciación Acumulada Edificios' WHEN [dbo].[movimientos].codigo LIKE '128%' THEN 'Terrenos' WHEN [dbo].[movimientos].codigo LIKE '129%' THEN 'Equipo de Servicios' WHEN [dbo].[movimientos].codigo LIKE '130%' THEN 'Depreciación acumulada de Eq. de Servicios' WHEN [dbo].[movimientos].codigo LIKE '140%' THEN 'Gastos de Organización' WHEN [dbo].[movimientos].codigo LIKE '141%' THEN 'Gastos de Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '142%' THEN 'Impuestos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '143%' THEN 'Gastos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '144%' THEN 'Deposito en Garantia' WHEN [dbo].[movimientos].codigo LIKE '150%' THEN 'Amortización Gastos Organización' WHEN [dbo].[movimientos].codigo LIKE '151%' THEN 'Amortización Gastos Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '200%' THEN 'PROVEEDORES' WHEN [dbo].[movimientos].codigo LIKE '201%' THEN 'ACREEDORES DIVERSOS' WHEN [dbo].[movimientos].codigo LIKE '202%' THEN 'IMPUESTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '203%' THEN 'DOCUMENTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '204%' THEN 'IVA Trasladado' WHEN [dbo].[movimientos].codigo LIKE '205%' THEN 'Anticipos de Clientes' WHEN [dbo].[movimientos].codigo LIKE '206%' THEN 'Sueldos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '207%' THEN 'Gastos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '208%' THEN 'PTU por Pagar' WHEN [dbo].[movimientos].codigo LIKE '220%' THEN 'Acreedores Hipotecarios' WHEN [dbo].[movimientos].codigo LIKE '221%' THEN 'Creditos Bancarios' WHEN [dbo].[movimientos].codigo LIKE '230%' THEN 'Intereses cobrados por adelantado' WHEN [dbo].[movimientos].codigo LIKE '000-030%' THEN 'CAPITAL' WHEN [dbo].[movimientos].codigo LIKE '000-031%' THEN 'Capital Social' WHEN [dbo].[movimientos].codigo LIKE '000-033%' THEN 'Resultado Ejercicios Anteriores' WHEN [dbo].[movimientos].codigo LIKE '000-034%' THEN 'Resultado del Ejercicio' WHEN [dbo].[movimientos].codigo LIKE '000-035%' THEN 'Utilidades Retenidas' ELSE 'Otros' END AS nombre, max([dbo].[movimientos].saldoInicial) - (SUM([dbo].[movimientos].abonos) - SUM([dbo].[movimientos].cargos)) as saldoAcumuladoActivo, max([dbo].[movimientos].saldoInicial) + (SUM([dbo].[movimientos].abonos) - SUM([dbo].[movimientos].cargos)) as saldoAcumuladoPasivo, min([dbo].[movimientos].saldoInicial) + (SUM([dbo].[movimientos].abonos) - SUM([dbo].[movimientos].cargos)) as saldoAcumuladoPasivoNegativo, min([dbo].[movimientos].saldoInicial) as saldoInicialMinimo FROM [dbo].[movimientos] WHERE idEmpresa_id = 3  GROUP BY  CASE WHEN [dbo].[movimientos].codigo LIKE '102%' THEN 'Bancos' WHEN [dbo].[movimientos].codigo LIKE '101%' THEN 'Caja' WHEN [dbo].[movimientos].codigo LIKE '100%' THEN 'Fondo Fijo Caja' WHEN [dbo].[movimientos].codigo LIKE '103%' THEN 'Clientes' WHEN [dbo].[movimientos].codigo LIKE '104%' THEN 'Documentos por Cobrar' WHEN [dbo].[movimientos].codigo LIKE '105%' THEN 'Deudores Diversos' WHEN [dbo].[movimientos].codigo LIKE '106%' THEN 'IVA Acreditable' WHEN [dbo].[movimientos].codigo LIKE '107%' THEN 'Funcionarios y Empleados' WHEN [dbo].[movimientos].codigo LIKE '108%' THEN 'Inventarios' WHEN [dbo].[movimientos].codigo LIKE '109%' THEN 'Anticipo a Proveedores' WHEN [dbo].[movimientos].codigo LIKE '120%' THEN 'Mobiliario y Equipo de oficina' WHEN [dbo].[movimientos].codigo LIKE '121%' THEN 'Depreciación Acumulada de Mob y Eq. oficina' WHEN [dbo].[movimientos].codigo LIKE '122%' THEN 'Equipo de Transporte' WHEN [dbo].[movimientos].codigo LIKE '123%' THEN 'Depreciación Acumulada Equipo Transporte' WHEN [dbo].[movimientos].codigo LIKE '124%' THEN 'Equipo de cómputo' WHEN [dbo].[movimientos].codigo LIKE '125%' THEN 'Depreciación acumulada Eq. cómputo' WHEN [dbo].[movimientos].codigo LIKE '126%' THEN 'Edificios' WHEN [dbo].[movimientos].codigo LIKE '127%' THEN 'Depreciación Acumulada Edificios' WHEN [dbo].[movimientos].codigo LIKE '128%' THEN 'Terrenos' WHEN [dbo].[movimientos].codigo LIKE '129%' THEN 'Equipo de Servicios' WHEN [dbo].[movimientos].codigo LIKE '130%' THEN 'Depreciación acumulada de Eq. de Servicios' WHEN [dbo].[movimientos].codigo LIKE '140%' THEN 'Gastos de Organización' WHEN [dbo].[movimientos].codigo LIKE '141%' THEN 'Gastos de Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '142%' THEN 'Impuestos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '143%' THEN 'Gastos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '144%' THEN 'Deposito en Garantia' WHEN [dbo].[movimientos].codigo LIKE '150%' THEN 'Amortización Gastos Organización' WHEN [dbo].[movimientos].codigo LIKE '151%' THEN 'Amortización Gastos Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '200%' THEN 'PROVEEDORES' WHEN [dbo].[movimientos].codigo LIKE '201%' THEN 'ACREEDORES DIVERSOS' WHEN [dbo].[movimientos].codigo LIKE '202%' THEN 'IMPUESTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '203%' THEN 'DOCUMENTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '204%' THEN 'IVA Trasladado' WHEN [dbo].[movimientos].codigo LIKE '205%' THEN 'Anticipos de Clientes' WHEN [dbo].[movimientos].codigo LIKE '206%' THEN 'Sueldos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '207%' THEN 'Gastos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '208%' THEN 'PTU por Pagar' WHEN [dbo].[movimientos].codigo LIKE '220%' THEN 'Acreedores Hipotecarios' WHEN [dbo].[movimientos].codigo LIKE '221%' THEN 'Creditos Bancarios' WHEN [dbo].[movimientos].codigo LIKE '230%' THEN 'Intereses cobrados por adelantado' WHEN [dbo].[movimientos].codigo LIKE '000-030%' THEN 'CAPITAL' WHEN [dbo].[movimientos].codigo LIKE '000-031%' THEN 'Capital Social' WHEN [dbo].[movimientos].codigo LIKE '000-033%' THEN 'Resultado Ejercicios Anteriores' WHEN [dbo].[movimientos].codigo LIKE '000-034%' THEN 'Resultado del Ejercicio' WHEN [dbo].[movimientos].codigo LIKE '000-035%' THEN 'Utilidades Retenidas' ELSE 'Otros' END").fetchall()
    for hola in json:
        print(hola, "este es hola")
    cnxn.commit()
    #cursor.close()
    return json


@api_view(['POST'])
def upload(request):
    xlsx_upload(request)
    init_db()
    dataframe_upload(df_listo)
    return Response({"Valor de linea 0 columna 0":df_listo.iat[0,0]})


def xlsx_upload(request):
    print(request.FILES['file'])
    df = pd.read_excel(request.FILES['file'])
    print (df)
    global df_listo
    df_listo = fix_df(df)
    # return df_listo

def init_db():
    server = 'finrep-server.database.windows.net' 
    database = 'FinRep-DB' 
    username = 'equipoelite' 
    password = 'CoffeeSoft-2022' 
    global cnxn
    # cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    global cursor
    cursor = cnxn.cursor()
    return cursor


def dataframe_upload(df):
    cursor = init_db()
    print("HOLA MAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    for index, row in df.iterrows():
        # print(row.id_empresa," ", row.codigo," ", row.nombre," ", row.concepto," ", row.referencia," ", float(row.saldo_inicial)," ", float(row.cargos)," ", float(row.abonos)," ", row.fecha)
        cursor.execute("INSERT INTO dbo.movimientos (idEmpresa_id,codigo,nombre,concepto,referencia,saldoInicial,cargos,abonos,fecha,codigoAgrupador,ingresoEgrego,nombreAgrupador,tipo) values(?,?,?,?,?,?,?,?,?,?,?,?,?)", row.id_empresa, row.codigo, row.nombre, row.concepto, row.referencia, float(row.saldo_inicial), float(row.cargos), float(row.abonos), row.fecha), row.codigo_agrupador, row.tipo, row.nombre_grupo, row.APC
    cnxn.commit()
    cursor.close()


@api_view(['GET'])
def balanceGeneral(request):
    jsonOp = {
                'activo': {
                    'circulante': [['Bancos', '6,181.41'],['Clientes', '2']],
                    'fijo': [['Uno', '1'], ['dos', '2']],
                    'diferido': [['jojo', '4'],['jeje', '5']]
                },
                'pasivo':{
                    'circulante': [['Bancos', '6,181.41'],['Clientes', '2']],
                    'fijo': [['Uno', '1'], ['dos', '2']],
                    'diferido': [['jojo', '4'],['jeje', '5']]
                }, 
                'capital': {
                    'capital': [['jujuju', '18']]
                }
            }
    return Response(jsonOp)

urlpatterns = [
    path('balanceGeneral', getMovimientos),
    path('xlsx',upload),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('flutter_web_app/', lambda r: flutter_redirect(r, 'index.html')),
    path('flutter_web_app/<path:resource>', flutter_redirect),
]

def es_agrupador(code):
        serie = catalogo.loc[catalogo['codigo'] == code]
        nivel = serie.loc[catalogo['nivel'] == 3]
        #print(nivel)
        if nivel.size > 0:
            tipo = nivel.iat[0, 3]
            return (True, tipo)
        else:
            return (False, 0)

def is_valid(row):
    if (row[1] != "" and pd.isna(row[2])==False):
        return True
    else:
        return False

def format_date(date):
    datetimeobject = datetime.strptime(date, '%d/%b/%Y')
    new_date = datetimeobject.strftime('%Y-%m-%d')
    return new_date

def fix_df(df):
    global catalogo
    catalogo = pd.read_excel('catalogo.xlsx')


    df.columns = ['fecha', 'tipo', 'numero', 'concepto', 'referencia', 'cargos', 'abonos', 'saldo']
    catalogo.columns = ['nivel', 'codigo', 'nombre', 'tipo', 'afectable', 'dig', 'edo', 'moneda', 'seg', 'rubro', 'agrupador']


    column_names = ['id_empresa', 'codigo', 'codigo_agrupador', 'nombre', 'nombre_grupo', 'tipo', 'APC', 'fecha', 'concepto', 'referencia', 'cargos', 'abonos', 'saldo', 'saldo_inicial']
    new_df = pd.DataFrame(columns = column_names)

    current_code = ""
    current_name = ""
    current_agrupador = ""
    current_saldoi = 0
    current_nombreG = ""
    current_APC = ""      
        
    count = 0
    for row in df.itertuples():
        if count > 6:        
            if (row[7] == 'Saldo inicial :'):
                agrupador = es_agrupador(row[1])
                if(agrupador[0]):
                    current_agrupador = row[1]
                    current_nombreG = row[2]
                    current_APC = agrupador[1]
                current_code = row[1]
                current_name = row[2]
                current_saldoi = row[8]
                fecha_inicial = datetime(2016, 6, 1)
                temp_df = {'id_empresa': 2, 'codigo': current_code, 'codigo_agrupador': current_agrupador, 'nombre': current_name,'nombre_grupo': current_nombreG,'tipo': "", 'APC': current_APC, 'fecha': '2016-06-01', 'concepto': '', 'referencia': '', 'cargos': 0.0, 'abonos': 0.0, 'saldo': 0.0, 'saldo_inicial': current_saldoi}
                new_df = new_df.append(temp_df, ignore_index=True)

            elif (is_valid(row)):
                new_date = format_date(row[1])

                if (pd.isna(row[6])):
                        cargos = 0.0
                else:
                    cargos = row[6]

                if (pd.isna(row[7])):
                    abonos = 0.0
                else:
                    abonos = row[7]

                if (pd.isna(row[7])):
                    saldo = 0.0
                else:
                    saldo = row[8]

                temp_df = {'id_empresa': 2, 'codigo': current_code, 'codigo_agrupador': current_agrupador, 'nombre': current_name,'nombre_grupo': current_nombreG,'tipo': row[2],'APC': current_APC, 'fecha': new_date, 'concepto': row[4], 'referencia': row[5], 'cargos': cargos, 'abonos': abonos, 'saldo': saldo, 'saldo_inicial': current_saldoi}
                new_df = new_df.append(temp_df, ignore_index=True)

        else:
            count = count + 1

    return new_df
    





