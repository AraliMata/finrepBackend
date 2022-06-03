from datetime import date
import pyodbc
import logging
"""
nombres stored procedures:

egresos @id_empresa
ingresos @id_empresa


"""

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
    

def valoresActivos(activo, codigos, activos):
    
    for val in activo:
        if val[1][1] <=  codigos[0][1][-2]:
            tipo = 'circulante'
        elif val[1][1] == codigos[1][1][-2]:
            tipo = 'fijo'
        else:
            tipo = 'diferido'

        if val[1][0:3] == '121':
            activos[tipo].append([val[0], round(-val[-1], 2)])
        else:
            activos[tipo].append([val[0], round(val[-1], 2)])


def valoresPasivos(pasivo, codigos, pasivos):
    for val in pasivo:
        if val[1][1] <= codigos[3][1][-2]:
            tipo = 'circulante'
        elif val[1][1] == codigos[4][1][-2]: 
            tipo = 'fijo'
        else:
            tipo = 'diferido'

        
        pasivos[tipo].append([val[0], round(val[-1], 2)])


def valoresCapital(capitalInf, capital):
    for val in capitalInf:
        capital['capital'].append([val[0], round(val[-1], 2)])

    capital['capital'].append(['Total CAPITAL', sum(list(zip(*capital['capital']))[1])])


def totalTipos(categoria, total, nombre):
    logging.debug('TotalTipos', categoria)
    categoria['circulante'].append(['Total CIRCULANTE', sum(list(zip(*categoria['circulante']))[1])])
    categoria['fijo'].append(['Total FIJO', sum(list(zip(*categoria['fijo']))[1])])
    categoria['diferido'].append(['Total DIFERIDO', sum(list(zip(*categoria['diferido']))[1])])
    categoria['diferido'].append([['SUMA DEL '+nombre], total])


def generarResponseBalanceGeneral(datos):
    print("Datos ", datos)
    balanceGeneral = {}
    movimientos = datos["movimientos"]
    codigos = datos["codes"]

    totalActivo = sum(list(zip(*movimientos['ActivoA']))[5]) + sum(list(zip(*movimientos['ActivoD']))[5]) - 2025 * 2
    totalPasivo = sum(list(zip(*movimientos['PasivoA']))[5]) 
    totalCapital = sum(list(zip(*movimientos['CapitalA']))[5]) 

    activos = {'circulante':[['', 0]], 'fijo': [['', 0]], 'diferido':[['', 0]]}
    pasivos = {'circulante':[['', 0]], 'fijo': [['', 0]], 'diferido':[['', 0]]}
    capital = {'capital': [['', 0]]}


    valoresActivos(movimientos['ActivoA'], codigos, activos)
    valoresActivos(movimientos['ActivoD'], codigos, activos)
    valoresPasivos(movimientos['PasivoA'], codigos, pasivos)
    valoresCapital(movimientos['CapitalA'], capital)
  
    totalTipos(activos, totalActivo, "ACTIVO")
    totalTipos(pasivos, totalPasivo, "PASIVO")

    capital['capital'].append(['SUMA DEL CAPITAL', sum(list(zip(*capital['capital']))[1])])
    capital['capital'].append(['SUMA DEL PASIVO Y CAPITAL', round(totalPasivo + totalCapital, 2)])

    balanceGeneral['activo'] = activos
    balanceGeneral['pasivo'] = pasivos
    balanceGeneral['capital'] = capital
    print("Balance general", balanceGeneral)
    return balanceGeneral


def movimientosBalance(idEmpresa):
    storedProc = {"PasivoA": "EXEC dbo.GetBalancePasivoAcreedora @empresaID = ?", 
    "ActivoA": "EXEC dbo.GetBalanceActivoAcreedora @empresaID = ?",
    "ActivoD": "EXEC dbo.GetBalanceActivoDeudora @empresaID = ?",
    "CapitalA": "EXEC dbo.GetBalanceCapitalAcreedora @empresaID = ?"}
    params = (idEmpresa)

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

def movimientosBalanceMes(idEmpresa, date_input):
    storedProc = {"PasivoA": "EXEC dbo.GetBalancePasivoAcreedoraMes @empresaID = ?, @fecha_input = ?", 
    "ActivoA": "EXEC dbo.GetBalanceActivoAcreedoraMes @empresaID = ?, @fecha_input = ?",
    "ActivoD": "EXEC dbo.GetBalanceActivoDeudoraMes @empresaID = ?, @fecha_input = ?",
    "CapitalA": "EXEC dbo.GetBalanceCapitalAcreedoraMes @empresaID = ?, @fecha_input = ?"}
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

def estadoResultados(idEmpresa):
    storedProc = {"ingresos": "EXEC dbo.ingresos @id_empresa = ?", "egresos": "EXEC dbo.egresos @id_empresa = ?"}

    params = (idEmpresa)
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

def estadoResultadosPeriodo(date_input):
    date_input = '2016-06-01'
    storedProc = {"ingresosInicial": "EXEC dbo.ingresosInicial @id_empresa = ?, @fecha_input = ?", 
    "ingresosPeriodo": "EXEC dbo.ingresosMes @id_empresa = ?, @fecha_input = ?",
    "egresosInicial": "EXEC dbo.egresosInicial @id_empresa = ?, @fecha_input = ?", 
    "egresosPeriodo": "EXEC dbo.egresosMes @id_empresa = ?, @fecha_input = ?"}
    params = (2, date_input)
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



def getCodigos(reporte, idEmpresa):
    if reporte == "BG":
        storedProc = "EXEC dbo.codigosBalanceGenral @id_empresa = ?"
    elif reporte == "ER":
        storedProc = "EXEC dbo.codigosEstadoresultados @id_empresa = ?"
    params = (idEmpresa)
    cursor = init_db()
    data = []
    datos = {}
    resultado = cursor.execute(storedProc, params)
    rows = cursor.fetchall()
    for row in rows:
        data.append(list(row))
    datos["codes"] = data
    return datos

def getBalanceCodigos(idEmpresa):
    data = movimientosBalance(idEmpresa)
    codes = getCodigos("BG", idEmpresa)
    result = {}
    result["codes"] = codes["codes"]
    result["movimientos"] = data
    print(result)
    return result

def getEstadoCodigos(idEmpresa):
    data = estadoResultados(idEmpresa)
    codes = getCodigos("ER", idEmpresa)
    result = {}
    result["codes"] = codes["codes"]
    result["movimientos"] = data
    print(result)
    return result


def getEstadoPeriodo(date_input):
    data = estadoResultadosPeriodo(date_input)
    codes = getCodigos("ER", 2)
    result = {}
    result["codes"] = codes["codes"]
    result["movimientos"] = data
    print(result)
    return result

