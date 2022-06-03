from re import A
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


def movimientosRelacionesAnaliticas(idEmpresa):
    storedProc = {"ActivoDeudora": "EXEC dbo.GetRAActivoDeudora @empresaID = ?",
    "ActivoAcreedora": "EXEC dbo.GetRAActivoAcreedor @empresaID = ?",
    "PasivoDeudora": "EXEC dbo.GetRAPasivoDeudora @empresaID = ?",
    "PasivoAcreedora": "EXEC dbo.GetRAPasivoAcreedora @empresaID = ?",
    "CapitalDeudora": "EXEC dbo.GetRACapitalDeudora @empresaID = ?",
    "CapitalAcreedora": "EXEC dbo.GetRACapitalAcreedora @empresaID = ?",
    "RAcreedora": "EXEC dbo.GetRelacionesAnaliticasRAcreedora @empresaID = ?",
    "RDeudora": "EXEC dbo.GetRelacionesAnaliticasRDedudora @empresaID = ?"
    }
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

    print("Movimientos relaciones analiticas:", datos)
    return datos


def getRelacionesCuentasMovimientos(idEmpresa=2):
    cuentas = movimientosBalance(idEmpresa)
    movimientos = movimientosRelacionesAnaliticas(idEmpresa)
    codes = getCodigosRA(idEmpresa)
    result = {}
    result["codes"] = codes["codes"]
    result["cuentas"] = cuentas
    result["movimientos"] = movimientos
    print(result)
    return result


def valoresActivos(activo, codigos, activos, codigosIndices, deudora, agrupadoresDatos):
    c, f = codigosIndices['circulanteActivo'], codigosIndices['fijoActivo']
    dA = "d" if deudora else "a"
    estilo = "se"
    saldoInicial = {'circulante':0, 'fijo':0, 'diferido':0}

    for val in activo:
        valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]

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
                valor = [val[2], val[0], round(dato[4], 2), round(dato[2], 2), round(dato[3], 2), round(dato[5], 2), estilo, dA]

        estilo = "se"

        saldoInicial[tipo] += valor[2]  #Saldo inicial
        activos[tipo][0][3] += valor[3] #Cargos
        activos[tipo][0][4] += valor[4] #Abonos
        activos[tipo].append(valor)
    
    activos['circulante'][0][2] += round(saldoInicial['circulante'],2) if deudora else round(activos['circulante'][0][2] - saldoInicial['circulante'],2)
    activos['fijo'][0][2] += round(saldoInicial['fijo'],2) if deudora else round(activos['fijo'][0][2] - saldoInicial['fijo'],2)
    activos['diferido'][0][2] += round(saldoInicial['diferido'],2) if deudora else round(activos['diferido'][0][2] - saldoInicial['diferido'],2)
    activos['circulante'][0][5] = round(activos['circulante'][0][2] + activos['circulante'][0][3] - activos['circulante'][0][4],2)
    activos['fijo'][0][5] = round(activos['fijo'][0][2] + activos['fijo'][0][3] - activos['fijo'][0][4],2)
    activos['diferido'][0][5] = round(activos['diferido'][0][2] + activos['diferido'][0][3] - activos['diferido'][0][4],2)


def valoresPasivos(pasivo, codigos, pasivos, codigosIndices, deudora, agrupadoresDatos):
    c, f = codigosIndices['circulantePasivo'], codigosIndices['fijoPasivo']
    dA = "d" if deudora else "a"
    estilo = "sq"
    saldoInicial = {'circulante':0, 'fijo':0, 'diferido':0}

    for val in pasivo:
        valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]

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
                valor = [val[2], val[0], round(dato[4], 2), round(dato[2], 2), round(dato[3], 2), round(dato[5], 2), estilo, dA]
           
        estilo = "se"

        saldoInicial[tipo] += valor[2] #Saldo inicial
        pasivos[tipo][0][3] += valor[3] #Cargos
        pasivos[tipo][0][4] += valor[4] #Abonos
        pasivos[tipo].append(valor)

    pasivos['circulante'][0][2] += round(saldoInicial['circulante'], 2) if deudora else round(pasivos['circulante'][0][2] - saldoInicial['circulante'], 2)
    pasivos['fijo'][0][2] += round(saldoInicial['fijo'], 2) if deudora else round(pasivos['fijo'][0][2] - saldoInicial['fijo'], 2)
    pasivos['diferido'][0][2] += round(saldoInicial['diferido'], 2) if deudora else round(pasivos['diferido'][0][2] - saldoInicial['diferido'], 2)
    pasivos['circulante'][0][5] = round(pasivos['circulante'][0][2] + pasivos['circulante'][0][3] - pasivos['circulante'][0][4], 2)
    pasivos['fijo'][0][5] = round(pasivos['fijo'][0][2] + pasivos['fijo'][0][3] - pasivos['fijo'][0][4], 2)
    pasivos['diferido'][0][5] = round(pasivos['diferido'][0][2] + pasivos['diferido'][0][3] - pasivos['diferido'][0][4], 2)


def valoresGeneral(datos, resultados, agrupadoresDatos, deudora, tipo):
    dA = "d" if deudora else "a"
    estilo = "se"
    saldoInicial, cargos, abonos = 0, 0, 0
    for val in datos:
        valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]

        if val[1] == val[2]:
            estilo = "n"
            if val[1] in agrupadoresDatos:
                dato = agrupadoresDatos[val[1]] 
                valor = [val[2], val[0], round(dato[4], 2), round(dato[2], 2), round(dato[3], 2), round(dato[5], 2)]
           
        estilo = "se"

        resultados.append(valor)
        saldoInicial += valor[2]
        cargos += valor[3]
        abonos += valor[4]
    
    saldoActual = saldoInicial - cargos + abonos if tipo == 1 else saldoInicial + cargos - abonos
    total = [resultados[0][0], resultados[0][1], round(saldoInicial, 2), round(cargos, 2), round(abonos, 2), round(saldoActual, 2), "se", dA]

    resultados[0] = total


def valoresCapital(datos, resultados, agrupadoresDatos, deudora):
    dA = "d" if deudora else "a"
    estilo = "se"
    saldoInicial, cargos, abonos = 0, 0, 0
    for val in datos:
        valor = [val[2], val[0], round(val[5], 2), round(val[3], 2), round(val[4], 2), round(val[6], 2), estilo, dA]

        if val[1] == val[2]:
            estilo = "n"
            if val[1] in agrupadoresDatos:
                dato = agrupadoresDatos[val[1]] 
                valor = [val[2], val[0], round(dato[4], 2), round(dato[2], 2), round(dato[3], 2), round(dato[5], 2), estilo, dA]
           
        estilo = "se"    
        
        resultados.append(valor)
        saldoInicial += valor[2]
        cargos += valor[3]
        abonos += valor[4]
    
    resultados[0][2] += round(saldoInicial, 2) if deudora else round(resultados[0][2] - saldoInicial, 2)


def getCodigosIndices(codigos):
    tipos = ["Activo", "Pasivo", "Resultados Acreedora", "Resultados Deudora"]

    tipo_indices = {}

    tipo_indices['circulanteActivo'] = 8
    tipo_indices['fijoActivo'] = 8
    tipo_indices['diferidoActivo'] = 8
    tipo_indices['circulantePasivo'] = 8
    tipo_indices['fijoPasivo'] = 8
    tipo_indices['diferidoPasivo'] = 8

    
    for i in range(len(codigos)):
        for tipo in tipos:
            if tipo in codigos[i][2]:
                tipo_indices[codigos[i][4].lower()+tipo] = i

    return tipo_indices


def getAgrupadorDatos(datos):
    agrupadoresDatos = {}

    for val in datos.values():
        for i in range(len(val)):
            agrupadoresDatos[val[i][1]] = val[i]

    return agrupadoresDatos


def totalTipos(datos, activo):
    saldoInicial = round(datos['circulante'][0][2] + datos['fijo'][0][2] + datos['diferido'][0][2], 2)
    cargos = round(datos['circulante'][0][3] + datos['fijo'][0][3] + datos['diferido'][0][3],2)
    abonos = round(datos['circulante'][0][4] + datos['fijo'][0][4] + datos['diferido'][0][4],2)
    saldoActual = round(saldoInicial + cargos - abonos,2) if activo else round(saldoInicial - cargos + abonos,2) 

    
    total = [[datos['total'][0][0], datos['total'][0][1], round(saldoInicial, 2), round(cargos, 2), round(abonos, 2), round(saldoActual, 2), "se", "d"]]
    datos['total'] = total

    
def totalCapital(datos):
    saldoActual = datos[0][2] + datos[0][3] - datos[0][4]

    datos[0][5] = round(saldoActual,2)


def getLista(datos):
    response = []
    for val in datos.values():
        response += val

    return response
        
    
def generarResponseRelacionesAnaliticas(datos):
    print("Datos ", datos)
    agrupadoresDatos, response = {}, {"movimientos":[], "totalCuentas":[['hi']], "sumasIguales":[['hi']]}
    movimientos = datos["movimientos"]
    cuentas = datos["cuentas"]
    codigos = datos["codes"]

    codigosIndices = getCodigosIndices(codigos)
    agrupadoresDatos = getAgrupadorDatos(cuentas)

    #CAMBIAR LO DE LA 0 en cada tipo
    cA, fA, dA = codigosIndices['circulanteActivo'], codigosIndices['fijoActivo'],  codigosIndices['diferidoActivo']
    cP, fP, dP =  codigosIndices['circulantePasivo'], codigosIndices['fijoPasivo'], codigosIndices['diferidoPasivo']
    activos = {'total':[['000-0100', "ACTIVO"]], 'circulante':[[codigos[cA][1], 'CIRCULANTE', 0, 0, 0,0, "se", "d"]], 'fijo': [[codigos[fA][1], 'FIJO', 0, 0, 0,0, "se", "d"]], 'diferido':[[codigos[dA][1], 'DIFERIDO', 0, 0, 0,0, "se", "d"]]}
    pasivos = {'total':[['000-0200', "PASIVO"]],'circulante':[[codigos[cP][1], 'CIRCULANTE', 0, 0, 0,0, "se", "d"]], 'fijo': [[codigos[fP][1], 'FIJO', 0, 0, 0,0, "se", "d"]], 'diferido':[[codigos[dP][1], 'DIFERIDO', 0, 0, 0,0, "se", "d"]]}
    capital = [['000-0300', 'CAPITAL', 0,0,0,0, "se", "d"]]
    RAcreedora = [['000-0400', 'RESULTADOS ACREEDORAS']]
    RDeudora = [['000-0500', 'RESULTADOS DEUDORAS']]

    valoresActivos(movimientos['ActivoDeudora'], codigos, activos, codigosIndices, True, agrupadoresDatos)
    valoresActivos(movimientos['ActivoAcreedora'], codigos, activos, codigosIndices, False, agrupadoresDatos)
    valoresPasivos(movimientos['PasivoDeudora'], codigos, pasivos, codigosIndices, True, agrupadoresDatos)
    valoresPasivos(movimientos['PasivoAcreedora'], codigos, pasivos, codigosIndices, False, agrupadoresDatos)
    valoresCapital(movimientos['CapitalDeudora'], capital, agrupadoresDatos, True)
    valoresCapital(movimientos['CapitalAcreedora'], capital, agrupadoresDatos, False)
    valoresGeneral(movimientos['RDeudora'], RDeudora, agrupadoresDatos, True, 0)
    valoresGeneral(movimientos['RAcreedora'], RAcreedora, agrupadoresDatos, False, 1)

    totalTipos(activos, True)
    totalTipos(pasivos, False)
    totalCapital(capital)

    response['movimientos'] = getLista(activos) + getLista(pasivos) + capital + RAcreedora + RDeudora

    print(response)
    
    return response

   