from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import APIView
from FinRepApp.Utils.relacionesAnaliticasFormatting import generarResponseRelacionesAnaliticas, getRelacionesCuentasMovimientos
from FinRepApp.Utils.periodos import mesesDispoibles
from FinRepApp.models import Cuentas
from .serializer import *
from .serializer import CuentasSerializer
from .serializer import UserSerializer
from rest_framework import viewsets
from rest_framework import status
from FinRepApp.Utils.balanceGeneralFormatting import *
from FinRepApp.Utils.estadoResultadosFormatting import *
from FinRepApp.Utils.fixingMovimientosDFToInsert import *
from FinRepApp.Utils.login import *
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# from FinRepApp.Utils.fixingMovimientosDFToInsert import df_listo
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
import json as js
import os
from django.views.static import serve
from rest_framework.decorators import action



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLUTTER_WEB_APP = os.path.join(BASE_DIR, 'flutter_web_app')

# Create your views here.
class Cuentas(viewsets.ModelViewSet):
    queryset = Cuentas.objects.all()
    serializer_class = CuentasSerializer


@api_view(['GET'])
def getMovimientos(request,idEmpresa, date_input):
    init_db()

    balance = getBalanceCodigos(idEmpresa, date_input)
    balanceGeneral = generarResponseBalanceGeneral(balance)
    # Serializing json  
    print("Balance: ", balanceGeneral)
    json_object = js.dumps(balanceGeneral)
    print(json_object) 
 
    return HttpResponse(js.dumps(balanceGeneral, ensure_ascii=False).encode("latin1"), content_type="application/json")

@api_view(['GET'])
def prueba(request):
    balance = movimientosBalanceMes(2, '2016-06-01')
    json_object = js.dumps(balance)
    print(json_object)
    return Response(balance)

class Usuario_EmpresaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Usuario_Empresa.objects.all()
    lookup_field = 'pk'
    # @action(methods=['get'], detail=False, url_path='empresas', url_name='empresas')
    @action(detail=True)
    def empresas(self, request, pk):
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

        """         
        json = {'empresas':{}}
        # json = {'empresas':{} , 'informacionStatus': []}
        for e in queryset:
            json['empresas'][e.idEmpresa.nombre] = e.idEmpresa.id 
        """

        json = []
        for e in queryset:
            json.append({'id':e.idEmpresa.id,'nombre':e.idEmpresa.nombre})
        return Response(json)
"""         # json = {'empresas':{} , 'informacionStatus': []}
        json = {}
        for e in queryset:
            json[e.idEmpresa.nombre] = e.idEmpresa.id
            # json['informacionStatus'][e.idEmpresa.nombre] = e.idUsuario.id
            # print(e.idUsuario.id)
 """
        
        # print(queryset.attribute)
        # serializer = Usuario_EmpresaSerializer(queryset, many=True)
        # serializer = Usuario_EmpresaSerializer(queryset)
        # print("jalo?")
        # if serializer.is_valid():
        #     print(serializer.data)
        # else:
        #     return Response(serializer.errors)




@api_view(['GET'])
def getEstadoResultados(request,idEmpresa,date_input=6):
    if date_input < 10:
        string = '0'+str(date_input)
    else:
        string = str(date_input)
    fecha = '2016-'+string+'-01'

    init_db()
    
    estadoResultados = generarResponseEstadoResultados(getEstadoPeriodo(idEmpresa,fecha))
    # Serializing json  

    #print(json, "JSON")
    # return Response({"Valor de linea 0 columna 0":df_listo.iat[0,0]})
    return HttpResponse(js.dumps(estadoResultados, ensure_ascii=False).encode("utf-8"), content_type="application/json")


@api_view(['GET'])
def getMeses(request):

    init_db()
    
    meses = generarResponseEstadoResultados(mesesDispoibles())
  
    return HttpResponse(js.dumps(meses, ensure_ascii=False), content_type="application/json")


@api_view(['GET'])
def getMovimientosTest(request,idEmpresa):
    print(idEmpresa, "esto es el idEmpresa")
    init_db()
    dictionary ={ 
    "id": "04", 
    "name": "sunil", 
    "department": "HR"
    } 
    balanceGeneral = []
    # Serializing json  
    json_object = js.dumps(balanceGeneral, sort_keys=True) 
    print(json_object)

    #print(json, "JSON")
    # return Response({"Valor de linea 0 columna 0":df_listo.iat[0,0]})
    return Response(json_object)

@api_view(['GET'])
def getRelacionesAnaliticas(request,idEmpresa):

    init_db()
    
    relacionesAnaliticas = generarResponseRelacionesAnaliticas(getRelacionesCuentasMovimientos(idEmpresa))
    # Serializing json  

    #print(json, "JSON")
    # return Response({"Valor de linea 0 columna 0":df_listo.iat[0,0]})
    return HttpResponse(js.dumps(relacionesAnaliticas, ensure_ascii=False).encode("utf-8"), content_type="application/json")

@api_view(['GET'])
def getEmpresas(request,idUsuario):
    pass


@api_view(['POST'])
def uploadMovimientos(request,idEmpresa):
    df_listo = readXlsxFile(request,idEmpresa)
    init_db()
    insertInDatabase(df_listo,idEmpresa)
    return Response({"Valor de linea 0 columna 0":df_listo.iat[0,0]})

def flutter_redirect(request, resource):
    return serve(request, resource, FLUTTER_WEB_APP)

def registerUser(request):
    resultadini = register(request)
    return resultadini
    #print("hola")
    #user = User.objects.create_user('Funcion', 'exito@hotmail.com', 'sisi')
    #llamar registro de login.py

# @api_view(['POST'])
# @permission_classes([AllowAny])
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def login(request):
    loginmarrano = my_view(request)
    return loginmarrano
