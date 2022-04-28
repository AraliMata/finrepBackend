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
from backendEmployeeTest.views import Employee
from FinRepApp import views
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.static import serve
import os
import pandas as pd

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
def xlsx_upload(request):
    print(request.FILES['file'])
    df = pd.read_excel(request.FILES['file'])
    print (df)
    return Response({"Valor de linea 0 columna 0":df.iat[0,0]})

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
    path('xlsx',xlsx_upload),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('flutter_web_app/', lambda r: flutter_redirect(r, 'index.html')),
    path('flutter_web_app/<path:resource>', flutter_redirect),
]


