import pyodbc
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
    
def acomodarResponse(movimientos):
    activos = {'circulante':[['', '']], 'fijo': [['', '']], 'diferido':[['', '']]}
    pasivos = {'circulante':[['', '']], 'fijo': [['', '']], 'diferido':[['', '']]}
    capital = {'capital': [['', '']]}

    sumasActivo = [0,0,0,0]
    sumasPasivo = [0,0,0,0]
    sumasCapital = [0,0,0]

    #6
    for movimiento in movimientos:
        if movimiento[2] != 0.0 and movimiento[1] != 'Otros':
            if movimiento[0][0] == '1':
                par = [movimiento[1], movimiento[2]]
                if movimiento[0][1] == '0':
                    activos['circulante'].append(par)
                    sumasActivo[0] += movimiento[2]
                elif movimiento[0][1] == '2':
                    if movimiento[0][2] == '1':
                        par = [movimiento[1], -(movimiento[2])]
                        activos['fijo'].append(par)
                        sumasActivo[1] += par[1]
                    else:
                        activos['fijo'].append(par)
                        sumasActivo[1] += par[1]
                elif movimiento[0][1] == '4': 
                    activos['diferido'].append(par)
                    sumasActivo[2] += movimiento[2]
            elif movimiento[0][0] == '2':
                if movimiento[5] < 0:
                    par = [movimiento[1], movimiento[4]]
                else:
                    par = [movimiento[1], movimiento[3]]

                if movimiento[0][1] == '0':
                    pasivos['circulante'].append(par)
                    # sumasPasivo[0] += movimiento[2]
                    sumasPasivo[0] += par[1]
                elif movimiento[0][1] == '2': 
                    pasivos['fijo'].append(par)
                    # sumasPasivo[1] += movimiento[2]
                    sumasPasivo[0] += par[1]
                elif movimiento[0][1] == '4': 
                    pasivos['diferido'].append(par)
                    # sumasPasivo[2] += movimiento[2]
                    sumasPasivo[0] += par[1]
            else:
                par = [movimiento[1], movimiento[2]]
                capital['capital'].append(par)
                sumasCapital[0] += movimiento[2]

    sumasActivo[3] = sum(sumasActivo[0:3])
    sumasPasivo[3] = sum(sumasPasivo[0:3])
    sumasCapital[1] = sumasCapital[0] + 115631.77
    sumasCapital[2] = sumasPasivo[3] + sumasCapital[1]

    activos['circulante'].append(['Total CIRCULANTE', sumasActivo[0]])
    activos['fijo'].append(['Total FIJO', sumasActivo[1]])
    activos['diferido'].append(['Total DIFERIDO', sumasActivo[2]])
    activos['diferido'].append(['SUMA DEL ACTIVO', sumasActivo[3]])

    pasivos['circulante'].append(['Total CIRCULANTE', sumasPasivo[0]])
    pasivos['fijo'].append(['Total FIJO', sumasPasivo[1]])
    pasivos['diferido'].append(['Total DIFERIDO', sumasPasivo[2]])
    pasivos['diferido'].append(['SUMA DEL PASIVO', sumasPasivo[3]])

    # capital['capital'].append(['Total CAPITAL', sumasCapital[0]])
    capital['capital'].append(['Total CAPITAL', sumasCapital[0]])
    capital['capital'].append(['Utilidad o Pérdida del Ejercicio', 115631.77])
    capital['capital'].append(['SUMA DEL CAPITAL', sumasCapital[1]])
    capital['capital'].append(['SUMA DEL PASIVO Y CAPITAL', sumasCapital[2]])
    
    balanceGeneral = {'activo': activos, 'pasivo': pasivos, 'capital':capital}
    print(balanceGeneral)
    return balanceGeneral


def movimientosBalance():
    storedProc = {"PasivoA": "EXEC dbo.GetBalancePasivoAcreedora @empresaID = ?", 
    "ActivoA": "EXEC dbo.GetBalanceActivoAcreedora @empresaID = ?",
    "ActivoD": "EXEC dbo.GetBalanceActivoDeudora @empresaID = ?",
    "CapitalA": "EXEC dbo.GetBalanceCapitalAcreedora @empresaID = ?"}
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

def estadoResultados():
    storedProc = {"ingresos": "EXEC dbo.ingresos @id_empresa = ?", "egresos": "EXEC dbo.egresos @id_empresa = ?"}

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

def getBalanceCodigos():
    data = movimientosBalance()
    codes = getCodigos("BG", 2)
    result = {}
    result["codes"] = codes["codes"]
    result["movimientos"] = data
    print(result)
    return result

def getEstadoCodigos():
    data = estadoResultados()
    codes = getCodigos("ER", 2)
    result = {}
    result["codes"] = codes["codes"]
    result["movimientos"] = data
    print(result)
    return result
