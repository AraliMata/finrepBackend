import unittest
from FinRepApp.Utils import balanceGeneralFormatting
from numpy import NaN

""" 
    Los archivos de pruebas deben terminar en _test.py
    Las funciones de las pruebas deben comenzar en test_
"""


class BalanceGeneralFormattingTest(unittest.TestCase):

    def test_json_generarBG(self):
        # Given
        input = { "codes": [ [ "CIRCULANTE", "000-0110", "A Activo Deudora" ], [ "FIJO", "000-0120", "A Activo Deudora" ], [ "DIFERIDO", "000-0140", "A Activo Deudora" ], [ "CIRCULANTE", "000-0210", "D Pasivo Acreedora" ], [ "FIJO", "000-0220", "D Pasivo Acreedora" ], [ "DIFERIDO", "000-0230", "D Pasivo Acreedora" ] ], "movimientos": { "PasivoA": [ [ "ACREEDORES DIVERSOS", "201-0000", 0.0, 0.0, -343.21, -343.21 ], [ "DOCUMENTOS POR PAGAR", "203-0000", 1282.33, 0.0, 96445.0, 95162.67 ], [ "IMPUESTOS POR PAGAR", "202-0000", 34920.0, 31510.28, 81786.53, 78376.81 ] ], "ActivoA": [ [ "Depreciación Acumulada de Mob y Eq. oficina", "121-0000", 0.0, 0.0, 2025.0, 2025.0 ] ], "ActivoD": [ [ "Bancos", "102-0000", 305064.14, 311967.68, 13084.95, 6181.410000000033 ], [ "Clientes", "103-0000", 217762.09, 295913.14, 254931.16, 176780.11 ], [ "Deudores Diversos", "105-0000", 0.0, 9151.0, 104485.37, 95334.37 ], [ "Impuestos Anticipados", "142-0000", 677.0, 0.0, 13757.0, 14434.0 ], [ "IVA Acreditable", "106-0000", 41383.19000000001, 33446.0, 34603.42, 42540.610000000015 ], [ "Mobiliario y Equipo de oficina", "120-0000", 0.0, 0.0, 14212.06, 14212.06 ] ], "CapitalA": [ [ "Capital Social", "000-0310", 0.0, 0.0, 100000.0, 100000.0 ], [ "Resultado Ejercicios Anteriores", "000-0330", 0.0, 0.0, -41370.48, -41370.48 ] ] } }
        # When
        answer = balanceGeneralFormatting.generarResponseBalanceGeneral(input)
        # Then
        #self.assertTrue(type(answer) is dict, "Debe dar True")
        self.assertEqual(True,False, answer)




