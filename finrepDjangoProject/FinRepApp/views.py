from django.shortcuts import render, redirect
from rest_framework.decorators import APIView
from FinRepApp.models import Cuentas
from .serializer import CuentasSerializer
from rest_framework import viewsets
from FinRepApp.Utils.balanceGeneralFormatting import *
from FinRepApp.Utils.fixingMovimientosDFToInsert import *
# from FinRepApp.Utils.fixingMovimientosDFToInsert import df_listo
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json as js
import os
from django.views.static import serve



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLUTTER_WEB_APP = os.path.join(BASE_DIR, 'flutter_web_app')

# Create your views here.
class Cuentas(viewsets.ModelViewSet):
    queryset = Cuentas.objects.all()
    serializer_class = CuentasSerializer


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

@api_view(['POST'])
def uploadMovimientos(request):
    df_listo = readXlsxFile(request)
    init_db()
    insertInDatabase(df_listo)
    return Response({"Valor de linea 0 columna 0":df_listo.iat[0,0]})

def flutter_redirect(request, resource):
    return serve(request, resource, FLUTTER_WEB_APP)