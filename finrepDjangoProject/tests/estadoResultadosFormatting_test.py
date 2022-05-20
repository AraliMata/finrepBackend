import unittest
from FinRepApp.Utils import estadoResultadosFormatting
from numpy import NaN

""" 
    Los archivos de pruebas deben terminar en _test.py
    Las funciones de las pruebas deben comenzar en test_
"""


class EstadoResultadosFormattingTest(unittest.TestCase):

    def test_json_generarER(self):
        # Given
        input = {"codes": [ [ 7, "401-0000", "H Resultados Acreedora", 2, "Productos Financieros" ], [ 8, "501-0000", "G Resultados Deudora", 2, "GASTOS DE SERVICIO" ], [ 9, "502-0000", "G Resultados Deudora", 2, "GASTOS FINANCIEROS" ], [ 10, "503-0000", "G Resultados Deudora", 2, "GASTOS ADMINISTRATIVOS" ], [ 11, "505-0000", "G Resultados Deudora", 2, "Compras" ] ], "movimientos": { "ingresos": [ [ "400-0000", 203544.34, "Servicios" ] ], "egresos": [ [ "501-0600", 57897.219999999994, "Servicio de Operacion" ], [ "502-1000", 1181.94, "COMISIONES BANCARIAS" ], [ "503-0180", 4241.46, "Mant de Eq de Transporte " ], [ "503-0190", 4720.29, "Arrendamiento " ], [ "503-0700", 4591.01, "Primas de seguro" ], [ "503-0800", 5047.07, "Luz" ], [ "503-1000", 499.48, "Papelería y Utíles" ], [ "503-1300", 2412.59, "Honorarios" ], [ "503-1400", 1899.85, "Gastos Correos y Teléfonos" ], [ "503-1500", 3909.74, "Gastos de Viaje" ], [ "503-1600", 6927.36, "Combustibles y Lubricantes " ], [ "503-2400", 14353.45, "Publicidad " ], [ "503-2500", 404.27, "Utiles de Aseo y Limpieza " ], [ "503-2700", 45914.54, "Asesoria Empresarial" ], [ "503-3700", 1229.1399999999999, "Dominios de Correos y Hosting" ], [ "503-3800", 1947.76, "Intereses " ], [ "503-9100", 5440.29, "Partidas no Deducibles" ], [ "503-9200", 3462.07, "Gastos Varios" ], [ "503-9300", 190.42, "Gastos No Deducibles" ], [ "505-0100", 102355.34, "COMPRAS" ] ] } }
        # When
        answer = estadoResultadosFormatting.generarResponseEstadoResultados(input)
        # Then
        #self.assertTrue(type(answer) is dict, "Debe dar True")
        self.assertEqual(True,False, answer)
