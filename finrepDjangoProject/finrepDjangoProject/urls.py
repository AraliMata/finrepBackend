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
import numpy as np
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


# global catalogo
# catalogo = pd.read_excel('catalogo.xlsx')

router = routers.DefaultRouter(trailing_slash=False)
router.register('employeedetails', Employee)
router.register('cuentas', views.Cuentas)
router.register('empresas', views.Usuario_EmpresaViewSet, basename='Usuario_EmpresaViewSet')
# router.register('cuentas', cuentas_list, basename='cuentas-list')
# recibirArchivoPost = views.recibirArchivo.as_view({'post': 'create'})
# router.register('xlsx', recibirArchivoPost)



urlpatterns = [
    path('balanceGeneral', views.getMovimientos),
    path('estadoResultados', views.getEstadoResultados),
    path('prueba', views.prueba),
    path('xlsx',views.uploadMovimientos),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('flutter_web_app/', lambda r: views.flutter_redirect(r, 'index.html')),
    path('flutter_web_app/<path:resource>', views.flutter_redirect),
    path('contabilidad/reportes/empresas/<int:idEmpresa>/balanceGeneral', views.getMovimientosTest),
    # path('contabilidad/usuarios/{idUsuario}/empresas', views.Usuario_EmpresaViewSet.as_view),
    # path('contabilidad/reportes/empresas/', views.getMovimientosTest),
]


    





