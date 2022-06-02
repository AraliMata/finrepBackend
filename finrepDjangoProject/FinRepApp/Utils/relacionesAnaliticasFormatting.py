from re import A
import pyodbc
import logging
from balanceGeneralFormatting import movimientosBalance

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

def cuentasEmpresa():
    storedProc = {"cuentas": "EXEC dbo.GetCuentasEmpresa @empresaID = ?"}
    params = (2)

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

def getCodigosRA(idEmpresa):
    storedProc = "EXEC dbo.codigosRelacionesAnaliticas @id_empresa = ?"
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


def movimientosRelacionesAnaliticas(empresaID):
    storedProc = {"ActivoDeudora": "EXEC dbo.GetRAActivoDeudora @empresaID = ?",
    "ActivoAcreedora": "EXEC dbo.GetRAActivoAcreedora @empresaID = ?",
    "PasivoDeudora": "EXEC dbo.GetRAPasivoDeudora @empresaID = ?",
    "PasivoAcreedora": "EXEC dbo.GetRAPasivoAcreedora @empresaID = ?",
    "CapitalDeudora": "EXEC dbo.GetRACapitalDeudora @empresaID = ?",
    "CapitalAcreedora": "EXEC dbo.GetRACapitalAcreedora @empresaID = ?",
    "RAcreedora": "EXEC dbo.GetRelacionesAnaliticaRAcreedora @empresaID = ?",
    "RDeudora": "EXEC dbo.GetRelacionesAnaliticaRDeudora @empresaID = ?"
    }
    params = (empresaID)

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

    print("Movimientos relaciones analiticas:", datos)
    return datos

def getRelacionesCuentasMovimientos(idEmpresa):
    cuentas = movimientosBalance()
    movimientos = movimientosRelacionesAnaliticas(idEmpresa)
    codes = getCodigosRA(2)
    result = {}
    result["codes"] = codes["codes"]
    result["cuentas"] = cuentas
    result["movimeintos"] = movimientos
    print(result)
    return result


def valoresActivos(activo, codigos, activos, codigosIndices, deudora, agrupadoresDatos):
    c, f = codigosIndices['circulanteActivo'], codigosIndices['fijoActivo']
    dA = "d" if deudora else "a"
    estilo = "se"

    for val in activo:
        valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), "se", dA]
        if val[1][1] <=  codigos[c][1][2]:
            tipo = 'circulante'
        elif val[1][1] == codigos[f][1][-2]:
            tipo = 'fijo'
        else:
            tipo = 'diferido'

        if val[1] == val[2]:
            estilo = "n"
            if val[1] in agrupadoresDatos:
                dato = agrupadoresDatos[val[1]] 
                valor = [val[2], val[0], round(dato[4], 2), round(dato[2], 2), round(dato[3], 2), round(dato[5], 2)]
            else:
                valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]
        else:
            valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]

        saldoInicial += valor[2]  #Saldo inicial
        activos[tipo][0][3] += valor[3] #Cargos
        activos[tipo][0][4] += valor[4] #Abonos
        activos[tipo].append(valor)
    
    activos[tipo][0][2] += saldoInicial if deudora else activos[tipo][0][2] - saldoInicial
    activos['circulante'][0][5] = activos['circulante'][0][2] + activos['circulante'][0][3] - activos['circulante'][0][4]
    activos['fijo'][0][5] = activos['fijo'][0][2] + activos['fijo'][0][3] - activos['fijo'][0][4]
    activos['diferido'][0][5] = activos['diferido'][0][2] + activos['diferido'][0][3] - activos['diferido'][0][4]


def valoresPasivos(pasivo, codigos, pasivos, codigosIndices, deudora, agrupadoresDatos):
    c, f = codigosIndices['circulantePasivo'], codigosIndices['fijoPasivo']
    dA = "d" if deudora else "a"
    estilo = "sq"
    
    for val in pasivo:
        if val[1][1] <= codigos[c][1][-2]:
            tipo = 'circulante'
        elif val[1][1] == codigos[f][1][-2]: 
            tipo = 'fijo'
        else:
            tipo = 'diferido'

        if val[1] == val[2]:
            estilo = "n"
            if val[1] in agrupadoresDatos:
                dato = agrupadoresDatos[val[1]] 
                valor = [val[2], val[0], round(dato[4], 2), round(dato[2], 2), round(dato[3], 2), round(dato[5], 2)]
            else:
                valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]
        else:
            estilo = "se"
            valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]

        saldoInicial += valor[2] #Saldo inicial
        pasivos[tipo][0][3] += valor[3] #Cargos
        pasivos[tipo][0][4] += valor[4] #Abonos
        pasivos[tipo].append(valor)

    pasivo[tipo][0][2] += saldoInicial if deudora else pasivo[tipo][0][2] - saldoInicial
    pasivos['circulante'][0][5] = pasivos['circulante'][0][2] + pasivos['circulante'][0][3] - pasivos['circulante'][0][4]
    pasivos['fijo'][0][5] = pasivos['fijo'][0][2] + pasivos['fijo'][0][3] - pasivos['fijo'][0][4]
    pasivos['diferido'][0][5] = pasivos['diferido'][0][2] + pasivos['diferido'][0][3] - pasivos['diferido'][0][4]

def valoresGeneral(datos, resultados, agrupadoresDatos, deudora, tipo):
    dA = "d" if deudora else "a"
    estilo = "se"
    saldoInicial, cargos, abonos = 0, 0, 0
    for val in datos:
        if val[1] == val[2]:
            estilo = "n"
            if val[1] in agrupadoresDatos:
                dato = agrupadoresDatos[val[1]] 
                valor = [val[2], val[0], round(dato[4], 2), round(dato[2], 2), round(dato[3], 2), round(dato[5], 2)]
            else:
                valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]
        else:
            estilo = "se"
            valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]
        
        resultados.append(valor)
        saldoInicial += valor[2]
        cargos += valor[3]
        abonos += valor[4]
    
    saldoActual = saldoInicial - cargos + abonos if tipo == 1 else saldoInicial + cargos - abonos
    total = [resultados[0][1], resultados[0][1], saldoInicial, cargos, abonos, saldoActual, "se", dA]

    resultados[0] = total

def valoresCapital(datos, resultados, agrupadoresDatos, deudora):
    dA = "d" if deudora else "a"
    estilo = "se"
    saldoInicial, cargos, abonos = 0, 0, 0
    for val in datos:
        if val[1] == val[2]:
            estilo = "n"
            if val[1] in agrupadoresDatos:
                dato = agrupadoresDatos[val[1]] 
                valor = [val[2], val[0], round(dato[4], 2), round(dato[2], 2), round(dato[3], 2), round(dato[5], 2)]
            else:
                valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]
        else:
            estilo = "se"
            valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]
        
        resultados.append(valor)
        saldoInicial += valor[2]
        cargos += valor[3]
        abonos += valor[4]
    
    resultados[0][2] += saldoInicial if deudora else resultados[0][2] - saldoInicial
    
def getCodigosIndices(codigos):
    tipos = ["Activo", "Pasivo", "Resultados Acreedora", "Resultados Deudora"]

    tipo_indices = {}
    for i in range(len(codigos)):
        for tipo in tipos:
            if tipo in codigos[i][2]:
                tipo_indices[codigos[i][4].toLower()+tipo] = i

def getAgrupadorDatos(datos):
    agrupadoresDatos = {}

    for val in datos.values():
        for i in range(len(val)):
            agrupadoresDatos[val[i][1]] = val[i]

def totalTipos(datos, activo):
    saldoInicial = datos['circulante'][2] + datos['fijo'][2] + datos['diferido'][2]
    cargos = datos['circulante'][3] + datos['fijo'][3] + datos['diferido'][3]
    abonos = datos['circulante'][4] + datos['fijo'][4] + datos['diferido'][4]
    saldoActual = saldoInicial + cargos - abonos if activo else saldoInicial - cargos + abonos 

    
    total = [datos['total'][0][0], datos['total'][0][1], saldoInicial, cargos, abonos, saldoActual, "se", "d"]
    datos['total'] = total

    
def totalCapital(datos):
    saldoActual = datos[0][2] + datos[0][3] - datos[0][4]

    datos[0][5] = saldoActual

def getLista(datos):
    response = []
    for val in datos.values:
        response += val
        
    
def generarResponseRelacionesAnaliticas(datos):
    print("Datos ", datos)
    agrupadoresDatos = {}
    movimientos = datos["movimientos"]
    cuentas = datos["cuentas"]
    codigos = datos["codes"]

    codigosIndices = getCodigosIndices(codigos)
    agrupadoresDatos = getAgrupadorDatos(cuentas)

    #CAMBIAR LO DE LA 0 en cada tipo
    cA, fA, dA = codigosIndices['circulanteActivo'], codigosIndices['fijoActivo'],  codigosIndices['diferidoActivo']
    cP, fP, dP =  codigosIndices['circulantePasivo'], codigosIndices['fijoPasivo'], codigosIndices['diferidoPasivo']
    activos = {'total':[['000-0100', "ACTIVO"]], 'circulante':[[codigos[cA][1], 'CIRCULANTE', 0, 0, 0,0]], 'fijo': [[codigos[fA][1], 'FIJO', 0, 0, 0,0]], 'diferido':[[codigos[dA][1], 'DIFERIDO', 0, 0, 0,0]]}
    pasivos = {'total':[['000-0200', "PASIVO"]],'circulante':[[codigos[cP][1], 'CIRCULANTE', 0, 0, 0,0]], 'fijo': [[codigos[fP][1], 'FIJO', 0, 0, 0,0]], 'diferido':[[codigos[dP][1], 'DIFERIDO', 0, 0, 0,0]]}
    capital = [['000-0300', 'CAPITAL', 0,0,0,0, "se", "d"]]
    RAcreedora = [['000-0500', 'RESULTADOS DEUDORES']]
    RDeudora = [['000-0400"', 'RESULTADOS ACREEDORES']]


    valoresActivos(movimientos['ActivoDeudora'], codigos, activos, codigosIndices, True, agrupadoresDatos)
    valoresActivos(movimientos['ActivoAcreedora'], codigos, activos, codigosIndices, False, agrupadoresDatos)
    valoresPasivos(movimientos['PasivoDeudora'], codigos, pasivos, codigosIndices, True, agrupadoresDatos)
    valoresPasivos(movimientos['PasivoAcreedora'], codigos, pasivos, codigosIndices, False, agrupadoresDatos)
    valoresCapital(movimientos['CapitalDeudora'], capital, agrupadoresDatos, True)
    valoresCapital(movimientos['CapitalAcreedora'], capital, agrupadoresDatos, False)
    valoresGeneral(movimientos['RDeudora'], RDeudora, agrupadoresDatos, True, 0)
    valoresGeneral(movimientos['RAcreedora'], RAcreedora, agrupadoresDatos, False, 1)

    response += getLista(activos) + getLista(pasivos) + capital + RAcreedora + RDeudora

    print(response)
    
    return response

   