from datetime import date
import pyodbc
import logging

from FinRepApp.Utils.balanceGeneralFormatting import *

def init_db():
    server = 'finrep-db-server.database.windows.net' 
    database = 'FinrepDB' 
    username = 'equipoelite' 
    password = 'CoffeeSoft-2022' 
    global cnxn
    # cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    global cursor
    cursor = cnxn.cursor()
    return cursor
    

def valoresIngresos(ingresos, ingresosPeriodo, ingresosAcumulado, totalIngresos):
    for i in range(len(ingresosPeriodo)):
        periodo = round(ingresosPeriodo[i][1],2)
        acumulado = round(ingresosAcumulado[i][1],2)
        porcentajeP = round(periodo * 100 / totalIngresos[0], 2)
        porcentajeA = round(acumulado * 100 / totalIngresos[1], 2)
        ingresos.append([ingresosPeriodo[i][0], periodo, porcentajeP, acumulado, porcentajeA])


def valoresEgresos(egresosPeriodo, egresosAcumulado, clasificaciones, totalIngresos):
    for i in range(len(egresosPeriodo)):
        periodo = round(egresosPeriodo[i][1], 2)
        acumulado = round(egresosAcumulado[i][1], 2)
        porcentajeP = round(periodo * 100 / totalIngresos[0], 2)
        porcentajeA = round(acumulado * 100 / totalIngresos[1], 2)

        for clasificacion in clasificaciones:
            if egresosPeriodo[i][3][0:3] == clasificacion[0][0:3]: 
                clasificacion[3].append([egresosPeriodo[i][0], periodo, porcentajeP, acumulado, porcentajeA])
                clasificacion[2] += periodo 
                clasificacion[4] += periodo 
    
        #egresos.append([egreso[2], periodo, porcentaje, periodo, porcentaje])

def crearClasificaciones(codigos):
    clasificaciones = []
    for codigo in codigos:
        clasificaciones.append([codigo[1], codigo[4], 0, [], 0])
        codigo.append(False)
    
    return clasificaciones


def agregarEgresos(estadoResultados, clasificaciones, totalIngresos):
    for clasificacion in clasificaciones:
        periodo = round(clasificacion[2], 2)
        porcentajeP = round(periodo * 100 / totalIngresos[0], 2)
        acumulado = round(clasificacion[4], 2)
        porcentajeA = round(acumulado * 100 / totalIngresos[1], 2)

        if(periodo != 0 or acumulado != 0):
            estadoResultados['egresos'].append([clasificacion[1], 0,0,0,0])

            for elem in clasificacion[3]:
                estadoResultados['egresos'].append(elem)

            estadoResultados['egresos'].append(['Total '+clasificacion[1], periodo, porcentajeP, acumulado, porcentajeA])

def getUtilidad(tip, tia, tep, tea):
    #totalIngresosP = sum(list(zip(*movimientos['ingresosPeriodo']))[1])
    #totalEgresosP = sum(list(zip(*movimientos['egresosPeriodo']))[1])
   
    totalIngresosP = tip
    totalEgresosP = tep
    totalIngresosA = tia
    totalEgresosA = tea

    periodo = round(totalIngresosP - totalEgresosP, 2)
    porcentajeP = round(periodo * 100 / totalIngresosP, 2)
    acumulado = round(totalIngresosA - totalEgresosA, 2)
    porcentajeA = round(acumulado * 100 / totalIngresosA, 2)
    return [periodo, porcentajeP, acumulado, porcentajeA]

def generarResponseEstadoResultados(datos):
    movimientos = datos['movimientos']
    codigos = datos['codes']
    estadoResultados = {'ingresos': [], 'egresos': []}
    totalIngresosPeriodo = sum(list(zip(*movimientos['ingresosPeriodo']))[1])
    totalIngresosAcumulado = sum(list(zip(*movimientos['ingresosAcumulado']))[1])
    totalEgresosPeriodo = sum(list(zip(*movimientos['egresosPeriodo']))[1])
    totalEgresosAcumulado = sum(list(zip(*movimientos['egresosAcumulado']))[1])
    clasificaciones = crearClasificaciones(codigos)

    totalIngresos = [totalIngresosPeriodo, totalIngresosAcumulado]
    
    valoresIngresos(estadoResultados['ingresos'], movimientos['ingresosPeriodo'], movimientos['ingresosAcumulado'], totalIngresos)
    valoresEgresos(movimientos['egresosPeriodo'], movimientos['egresosAcumulado'], clasificaciones, totalIngresos)
    agregarEgresos(estadoResultados, clasificaciones, totalIngresos)

    estadoResultados['ingresos'].append(['Total Ingresos', round(totalIngresosPeriodo, 2), 100, round(totalIngresosAcumulado, 2), 100])
    estadoResultados['egresos'].append(['Total Egresos', round(totalEgresosPeriodo, 2), 
                                        round(totalEgresosPeriodo * 100 / totalIngresosPeriodo, 2), 
                                        round(totalEgresosAcumulado, 2), round(totalEgresosAcumulado * 100 / totalIngresosAcumulado, 2)])
    estadoResultados['egresos'].append(['Utilidad (o Pérdida)'] + getUtilidad(totalIngresosPeriodo, totalIngresosAcumulado, totalEgresosPeriodo, totalEgresosAcumulado))

    return estadoResultados
  

def estadoResultadosPeriodo(idEmpresa=2, date_input='2016-06-01'):
    storedProc = {"ingresosAcumulado": "EXEC dbo.ingresosInicial @id_empresa = ?, @fecha_input = ?", 
    "ingresosPeriodo": "EXEC dbo.ingresosMes @id_empresa = ?, @fecha_input = ?",
    "egresosAcumulado": "EXEC dbo.egresosInicial2 @id_empresa = ?, @fecha_input = ?", 
    "egresosPeriodo": "EXEC dbo.egresosMes2 @id_empresa = ?, @fecha_input = ?"}
    params = (idEmpresa, date_input)
    cursor = init_db()
    data = []
    datos = {}
    for tipo in storedProc:
        resultado = cursor.execute(storedProc[tipo], params)
        rows = cursor.fetchall()
        for row in rows:
            data.append(list(row))
        datos[tipo] = data
        data = []

    print(datos)
    return datos

def getEstadoPeriodo(idEmpresa, date_input='2016-06-01'):
    data = estadoResultadosPeriodo(date_input)
    codes = getCodigos("ER", idEmpresa)
    result = {}
    result["codes"] = codes["codes"]
    result["movimientos"] = data
    print(result)
    return result