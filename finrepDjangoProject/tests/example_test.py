import unittest
from FinRepApp.Utils import fixingMovimientosDFToInsert
from numpy import NaN

""" 
    Los archivos de pruebas deben terminar en _test.py
    Las funciones de las pruebas deben comenzar en test_
"""

class fixingMovimientosDFToInsertTest(unittest.TestCase):

    def test_is_valid_valor_null(self):
        row = [0,"hola",NaN]
        res = fixingMovimientosDFToInsert.is_valid(row)
        self.assertEqual(False,res,"Debe dar false")