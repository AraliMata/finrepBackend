from rest_framework.response import Response
from rest_framework.decorators import api_view



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