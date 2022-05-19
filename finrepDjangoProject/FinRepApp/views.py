from django.shortcuts import render, redirect
from rest_framework.decorators import APIView
from FinRepApp.models import Cuentas
from .serializer import *
from rest_framework import viewsets
from FinRepApp.Utils.balanceGeneralFormatting import *
from FinRepApp.Utils.fixingMovimientosDFToInsert import *
from FinRepApp.Utils.login import *
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
def prueba(request):
    balance = getEstadoCodigos()
    json_object = js.dumps(balance)
    print(json_object)
    return Response(balance)

class Usuario_EmpresaViewSet(viewsets.ViewSet):
    queryset = Usuario_Empresa.objects.all()

    def retrieve(self, request, pk):
        for e in Usuario_Empresa.objects.all():
            print(e)
        print(pk, "esto es el pk")
        # queryset = Usuario_Empresa.objects.filter(idUsuario_id=pk).only('idEmpresa')
        queryset = Usuario_Empresa.objects.filter(idUsuario_id=pk)
        print(queryset.count(), "cuenta de queryset")
        # no usar serializer tal vez, puedo únicamente convertir los nombres directamente en un JSON
        # devolver solo el nombre no sé si esté bien porque hay que tener el id tal vez más bien o guardarlo en alguna variable
        # o algo así para poder usarlo luego en los reportes y la subida de archivo
        # {
        # empresas:{"Lecar":1, "Walmart":3, "Ereh":3} , 
        # informaciónStatus: [] 
        # }
        json = {'empresas':{} , 'status': []}
        # json = {'empresas':{} , 'informacionStatus': []}
        for e in queryset:
            json['empresas'][e.idEmpresa.nombre] = e.idEmpresa.id
            # json['informacionStatus'][e.idEmpresa.nombre] = e.idUsuario.id
            # print(e.idUsuario.id)

        
        # print(queryset.attribute)
        # serializer = Usuario_EmpresaSerializer(queryset, many=True)
        # serializer = Usuario_EmpresaSerializer(queryset)
        return Response(json)
        print("jalo?")
        if serializer.is_valid():
            print(serializer.data)
        else:
            return Response(serializer.errors)

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

@api_view(['GET'])
def getMovimientosTest(request,idEmpresa):
    print(idEmpresa, "esto es el idEmpresa")
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

@api_view(['GET'])
def getEmpresas(request,idUsuario):
    pass


@api_view(['POST'])
def uploadMovimientos(request):
    df_listo = readXlsxFile(request)
    init_db()
    insertInDatabase(df_listo)
    return Response({"Valor de linea 0 columna 0":df_listo.iat[0,0]})

def flutter_redirect(request, resource):
    return serve(request, resource, FLUTTER_WEB_APP)

def registerUser(request):
    resultadini = register(request)
    return resultadini
    #print("hola")
    #user = User.objects.create_user('Funcion', 'exito@hotmail.com', 'sisi')
    #llamar registro de login.py
def login(request):
    loginmarrano = my_view(request)
    return loginmarrano
