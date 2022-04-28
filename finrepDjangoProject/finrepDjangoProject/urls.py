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


# cuentas_list = views.Cuentas.as_view({
#     'get': 'list'
# })
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


@api_view(['POST'])
def upload(request):
    df = xlsx_upload(request)
    init_db()
    dataframe_upload(df)


def xlsx_upload(request):
    print(request.FILES['file'])
    df = pd.read_excel(request.FILES['file'])
    print (df)
    global df_listo
    df_listo = fix_df(df)
    return df_listo
    #return Response({"Valor de linea 0 columna 0":df.iat[0,0]})

def init_db():
    server = 'finrep-server.database.windows.net' 
    database = 'FinRep-DB' 
    username = 'equipoelite' 
    password = 'CoffeeSoft-2022' 
    global cnxn
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    global cursor
    cursor = cnxn.cursor()
    return cursor


def dataframe_upload(df):
    cursor = init_db()
    for index, row in df.iterrows():
     cursor.execute("INSERT INTO FinRep-DB.movimientos (idEmpresa_id,codigo,nombre,concepto,referencia,saldoInicial,cargos,abonos,fecha) values(?,?,?,?,?,?,?,?)", row.id_empresa, row.codigo, row.nombre, row.concepto, row.referencia, row.saldo_inicial, row.cargos, row.abonos, row.fecha)
    cnxn.commit()
    cursor.close()


@api_view(['GET'])
def balanceGeneral(request):
    jsonOp = {
                'activo': {
                    'circulante': [['Bancos', 6,181.41],['Clientes', 2]],
                    'fijo': [['Uno', 1], ['dos', 2]],
                    'diferido': [['jojo', 4],['jeje', 5]]
                },
                'pasivo':{
                    'circulante': [['Bancos', 6,181.41],['Clientes', 2]],
                    'fijo': [['Uno', 1], ['dos', 2]],
                    'diferido': [['jojo', 4],['jeje', 5]]
                }, 
                'capital': {
                    'capital': [['jujuju', 18]]
                }
            }
    return Response(jsonOp)

urlpatterns = [
    path('balanceGeneral',balanceGeneral),
    path('xlsx',upload),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('flutter_web_app/', lambda r: flutter_redirect(r, 'index.html')),
    path('flutter_web_app/<path:resource>', flutter_redirect),
]

def fix_df(df):
    df.columns = ['fecha', 'tipo', 'numero', 'concepto', 'referencia', 'cargos', 'abonos', 'saldo']

    column_names = ['id_empresa', 'codigo', 'nombre', 'fecha', 'concepto', 'referencia', 'cargos', 'abonos', 'saldo', 'saldo_inicial']
    new_df = pd.DataFrame(columns = column_names)

    current_code = ""
    current_name = ""
    current_saldoi = 0

    """
    1: fecha
    2: tipo
    3: numero
    4: concepto
    5: referencia
    6: cargos
    7: abonos
    8: saldo
    """
    count = 0
    for row in df.itertuples():
        if count > 6:
            if (row[7] == 'Saldo inicial :'):
                current_code = row[1]
                current_name = row[2]
                current_saldoi = row[8]
                fecha_inicial = datetime(2016, 6, 1)
                temp_df = {'id_empresa': 2, 'codigo': current_code, 'nombre': current_name, 'fecha': '2016-06-01', 'concepto': '', 'referencia': '', 'cargos': 0.0, 'abonos': 0.0, 'saldo': 0.0, 'saldo_inicial': current_saldoi}
                new_df = new_df.append(temp_df, ignore_index=True)

            elif (row[1] != "" and pd.isna(row[2])==False):
                date_input = row[1]
                datetimeobject = datetime.strptime(date_input, '%d/%b/%Y')
                new_date = datetimeobject.strftime('%Y-%m-%d')
                
                temp_df = {'id_empresa': 2, 'codigo': current_code, 'nombre': current_name, 'fecha': new_date, 'concepto': row[4], 'referencia': row[5], 'cargos': row[6], 'abonos': row[7], 'saldo': row[8], 'saldo_inicial': current_saldoi}
                new_df = new_df.append(temp_df, ignore_index=True)
        else:
            count = count + 1

    #print(new_df['fecha'].head())
    return new_df





