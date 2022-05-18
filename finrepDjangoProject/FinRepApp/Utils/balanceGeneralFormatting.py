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

def movimientoshacker():
    cursor = init_db()
    print("HOLA MAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #json = cursor.execute("SELECT * FROM [dbo].[movimientos]").fetchall()
    # json = cursor.execute("SELECT min([dbo].[movimientos].codigo) as codigo, CASE WHEN [dbo].[movimientos].codigo LIKE '102%' THEN 'Bancos' WHEN [dbo].[movimientos].codigo LIKE '101%' THEN 'Caja' WHEN [dbo].[movimientos].codigo LIKE '100%' THEN 'Fondo Fijo Caja' WHEN [dbo].[movimientos].codigo LIKE '103%' THEN 'Clientes' WHEN [dbo].[movimientos].codigo LIKE '104%' THEN 'Documentos por Cobrar' WHEN [dbo].[movimientos].codigo LIKE '105%' THEN 'Deudores Diversos' WHEN [dbo].[movimientos].codigo LIKE '106%' THEN 'IVA Acreditable' WHEN [dbo].[movimientos].codigo LIKE '107%' THEN 'Funcionarios y Empleados' WHEN [dbo].[movimientos].codigo LIKE '108%' THEN 'Inventarios' WHEN [dbo].[movimientos].codigo LIKE '109%' THEN 'Anticipo a Proveedores' WHEN [dbo].[movimientos].codigo LIKE '120%' THEN 'Mobiliario y Equipo de oficina' WHEN [dbo].[movimientos].codigo LIKE '121%' THEN 'Depreciación Acumulada de Mob y Eq. oficina' WHEN [dbo].[movimientos].codigo LIKE '122%' THEN 'Equipo de Transporte' WHEN [dbo].[movimientos].codigo LIKE '123%' THEN 'Depreciación Acumulada Equipo Transporte' WHEN [dbo].[movimientos].codigo LIKE '124%' THEN 'Equipo de cómputo' WHEN [dbo].[movimientos].codigo LIKE '125%' THEN 'Depreciación acumulada Eq. cómputo' WHEN [dbo].[movimientos].codigo LIKE '126%' THEN 'Edificios' WHEN [dbo].[movimientos].codigo LIKE '127%' THEN 'Depreciación Acumulada Edificios' WHEN [dbo].[movimientos].codigo LIKE '128%' THEN 'Terrenos' WHEN [dbo].[movimientos].codigo LIKE '129%' THEN 'Equipo de Servicios' WHEN [dbo].[movimientos].codigo LIKE '130%' THEN 'Depreciación acumulada de Eq. de Servicios' WHEN [dbo].[movimientos].codigo LIKE '140%' THEN 'Gastos de Organización' WHEN [dbo].[movimientos].codigo LIKE '141%' THEN 'Gastos de Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '142%' THEN 'Impuestos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '143%' THEN 'Gastos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '144%' THEN 'Deposito en Garantia' WHEN [dbo].[movimientos].codigo LIKE '150%' THEN 'Amortización Gastos Organización' WHEN [dbo].[movimientos].codigo LIKE '151%' THEN 'Amortización Gastos Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '200%' THEN 'PROVEEDORES' WHEN [dbo].[movimientos].codigo LIKE '201%' THEN 'ACREEDORES DIVERSOS' WHEN [dbo].[movimientos].codigo LIKE '202%' THEN 'IMPUESTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '203%' THEN 'DOCUMENTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '204%' THEN 'IVA Trasladado' WHEN [dbo].[movimientos].codigo LIKE '205%' THEN 'Anticipos de Clientes' WHEN [dbo].[movimientos].codigo LIKE '206%' THEN 'Sueldos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '207%' THEN 'Gastos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '208%' THEN 'PTU por Pagar' WHEN [dbo].[movimientos].codigo LIKE '220%' THEN 'Acreedores Hipotecarios' WHEN [dbo].[movimientos].codigo LIKE '221%' THEN 'Creditos Bancarios' WHEN [dbo].[movimientos].codigo LIKE '230%' THEN 'Intereses cobrados por adelantado' WHEN [dbo].[movimientos].codigo LIKE '000-030%' THEN 'CAPITAL' WHEN [dbo].[movimientos].codigo LIKE '000-031%' THEN 'Capital Social' WHEN [dbo].[movimientos].codigo LIKE '000-033%' THEN 'Resultado Ejercicios Anteriores' WHEN [dbo].[movimientos].codigo LIKE '000-034%' THEN 'Resultado del Ejercicio' WHEN [dbo].[movimientos].codigo LIKE '000-035%' THEN 'Utilidades Retenidas' ELSE 'Otros' END AS nombre, max([dbo].[movimientos].saldoInicial) - (SUM([dbo].[movimientos].abonos) - SUM([dbo].[movimientos].cargos)) as saldoAcumulado FROM [dbo].[movimientos] WHERE idEmpresa_id = 3  GROUP BY  CASE WHEN [dbo].[movimientos].codigo LIKE '102%' THEN 'Bancos' WHEN [dbo].[movimientos].codigo LIKE '101%' THEN 'Caja' WHEN [dbo].[movimientos].codigo LIKE '100%' THEN 'Fondo Fijo Caja' WHEN [dbo].[movimientos].codigo LIKE '103%' THEN 'Clientes' WHEN [dbo].[movimientos].codigo LIKE '104%' THEN 'Documentos por Cobrar' WHEN [dbo].[movimientos].codigo LIKE '105%' THEN 'Deudores Diversos' WHEN [dbo].[movimientos].codigo LIKE '106%' THEN 'IVA Acreditable' WHEN [dbo].[movimientos].codigo LIKE '107%' THEN 'Funcionarios y Empleados' WHEN [dbo].[movimientos].codigo LIKE '108%' THEN 'Inventarios' WHEN [dbo].[movimientos].codigo LIKE '109%' THEN 'Anticipo a Proveedores' WHEN [dbo].[movimientos].codigo LIKE '120%' THEN 'Mobiliario y Equipo de oficina' WHEN [dbo].[movimientos].codigo LIKE '121%' THEN 'Depreciación Acumulada de Mob y Eq. oficina' WHEN [dbo].[movimientos].codigo LIKE '122%' THEN 'Equipo de Transporte' WHEN [dbo].[movimientos].codigo LIKE '123%' THEN 'Depreciación Acumulada Equipo Transporte' WHEN [dbo].[movimientos].codigo LIKE '124%' THEN 'Equipo de cómputo' WHEN [dbo].[movimientos].codigo LIKE '125%' THEN 'Depreciación acumulada Eq. cómputo' WHEN [dbo].[movimientos].codigo LIKE '126%' THEN 'Edificios' WHEN [dbo].[movimientos].codigo LIKE '127%' THEN 'Depreciación Acumulada Edificios' WHEN [dbo].[movimientos].codigo LIKE '128%' THEN 'Terrenos' WHEN [dbo].[movimientos].codigo LIKE '129%' THEN 'Equipo de Servicios' WHEN [dbo].[movimientos].codigo LIKE '130%' THEN 'Depreciación acumulada de Eq. de Servicios' WHEN [dbo].[movimientos].codigo LIKE '140%' THEN 'Gastos de Organización' WHEN [dbo].[movimientos].codigo LIKE '141%' THEN 'Gastos de Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '142%' THEN 'Impuestos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '143%' THEN 'Gastos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '144%' THEN 'Deposito en Garantia' WHEN [dbo].[movimientos].codigo LIKE '150%' THEN 'Amortización Gastos Organización' WHEN [dbo].[movimientos].codigo LIKE '151%' THEN 'Amortización Gastos Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '200%' THEN 'PROVEEDORES' WHEN [dbo].[movimientos].codigo LIKE '201%' THEN 'ACREEDORES DIVERSOS' WHEN [dbo].[movimientos].codigo LIKE '202%' THEN 'IMPUESTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '203%' THEN 'DOCUMENTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '204%' THEN 'IVA Trasladado' WHEN [dbo].[movimientos].codigo LIKE '205%' THEN 'Anticipos de Clientes' WHEN [dbo].[movimientos].codigo LIKE '206%' THEN 'Sueldos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '207%' THEN 'Gastos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '208%' THEN 'PTU por Pagar' WHEN [dbo].[movimientos].codigo LIKE '220%' THEN 'Acreedores Hipotecarios' WHEN [dbo].[movimientos].codigo LIKE '221%' THEN 'Creditos Bancarios' WHEN [dbo].[movimientos].codigo LIKE '230%' THEN 'Intereses cobrados por adelantado' WHEN [dbo].[movimientos].codigo LIKE '000-030%' THEN 'CAPITAL' WHEN [dbo].[movimientos].codigo LIKE '000-031%' THEN 'Capital Social' WHEN [dbo].[movimientos].codigo LIKE '000-033%' THEN 'Resultado Ejercicios Anteriores' WHEN [dbo].[movimientos].codigo LIKE '000-034%' THEN 'Resultado del Ejercicio' WHEN [dbo].[movimientos].codigo LIKE '000-035%' THEN 'Utilidades Retenidas' ELSE 'Otros' END").fetchall()
    json = cursor.execute("SELECT min([dbo].[movimientos].codigo) as codigo, CASE WHEN [dbo].[movimientos].codigo LIKE '102%' THEN 'Bancos' WHEN [dbo].[movimientos].codigo LIKE '101%' THEN 'Caja' WHEN [dbo].[movimientos].codigo LIKE '100%' THEN 'Fondo Fijo Caja' WHEN [dbo].[movimientos].codigo LIKE '103%' THEN 'Clientes' WHEN [dbo].[movimientos].codigo LIKE '104%' THEN 'Documentos por Cobrar' WHEN [dbo].[movimientos].codigo LIKE '105%' THEN 'Deudores Diversos' WHEN [dbo].[movimientos].codigo LIKE '106%' THEN 'IVA Acreditable' WHEN [dbo].[movimientos].codigo LIKE '107%' THEN 'Funcionarios y Empleados' WHEN [dbo].[movimientos].codigo LIKE '108%' THEN 'Inventarios' WHEN [dbo].[movimientos].codigo LIKE '109%' THEN 'Anticipo a Proveedores' WHEN [dbo].[movimientos].codigo LIKE '120%' THEN 'Mobiliario y Equipo de oficina' WHEN [dbo].[movimientos].codigo LIKE '121%' THEN 'Depreciación Acumulada de Mob y Eq. oficina' WHEN [dbo].[movimientos].codigo LIKE '122%' THEN 'Equipo de Transporte' WHEN [dbo].[movimientos].codigo LIKE '123%' THEN 'Depreciación Acumulada Equipo Transporte' WHEN [dbo].[movimientos].codigo LIKE '124%' THEN 'Equipo de cómputo' WHEN [dbo].[movimientos].codigo LIKE '125%' THEN 'Depreciación acumulada Eq. cómputo' WHEN [dbo].[movimientos].codigo LIKE '126%' THEN 'Edificios' WHEN [dbo].[movimientos].codigo LIKE '127%' THEN 'Depreciación Acumulada Edificios' WHEN [dbo].[movimientos].codigo LIKE '128%' THEN 'Terrenos' WHEN [dbo].[movimientos].codigo LIKE '129%' THEN 'Equipo de Servicios' WHEN [dbo].[movimientos].codigo LIKE '130%' THEN 'Depreciación acumulada de Eq. de Servicios' WHEN [dbo].[movimientos].codigo LIKE '140%' THEN 'Gastos de Organización' WHEN [dbo].[movimientos].codigo LIKE '141%' THEN 'Gastos de Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '142%' THEN 'Impuestos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '143%' THEN 'Gastos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '144%' THEN 'Deposito en Garantia' WHEN [dbo].[movimientos].codigo LIKE '150%' THEN 'Amortización Gastos Organización' WHEN [dbo].[movimientos].codigo LIKE '151%' THEN 'Amortización Gastos Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '200%' THEN 'PROVEEDORES' WHEN [dbo].[movimientos].codigo LIKE '201%' THEN 'ACREEDORES DIVERSOS' WHEN [dbo].[movimientos].codigo LIKE '202%' THEN 'IMPUESTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '203%' THEN 'DOCUMENTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '204%' THEN 'IVA Trasladado' WHEN [dbo].[movimientos].codigo LIKE '205%' THEN 'Anticipos de Clientes' WHEN [dbo].[movimientos].codigo LIKE '206%' THEN 'Sueldos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '207%' THEN 'Gastos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '208%' THEN 'PTU por Pagar' WHEN [dbo].[movimientos].codigo LIKE '220%' THEN 'Acreedores Hipotecarios' WHEN [dbo].[movimientos].codigo LIKE '221%' THEN 'Creditos Bancarios' WHEN [dbo].[movimientos].codigo LIKE '230%' THEN 'Intereses cobrados por adelantado' WHEN [dbo].[movimientos].codigo LIKE '000-030%' THEN 'CAPITAL' WHEN [dbo].[movimientos].codigo LIKE '000-031%' THEN 'Capital Social' WHEN [dbo].[movimientos].codigo LIKE '000-033%' THEN 'Resultado Ejercicios Anteriores' WHEN [dbo].[movimientos].codigo LIKE '000-034%' THEN 'Resultado del Ejercicio' WHEN [dbo].[movimientos].codigo LIKE '000-035%' THEN 'Utilidades Retenidas' ELSE 'Otros' END AS nombre, max([dbo].[movimientos].saldoInicial) - (SUM([dbo].[movimientos].abonos) - SUM([dbo].[movimientos].cargos)) as saldoAcumuladoActivo, max([dbo].[movimientos].saldoInicial) + (SUM([dbo].[movimientos].abonos) - SUM([dbo].[movimientos].cargos)) as saldoAcumuladoPasivo, min([dbo].[movimientos].saldoInicial) + (SUM([dbo].[movimientos].abonos) - SUM([dbo].[movimientos].cargos)) as saldoAcumuladoPasivoNegativo, min([dbo].[movimientos].saldoInicial) as saldoInicialMinimo FROM [dbo].[movimientos] WHERE idEmpresa_id = 3  GROUP BY  CASE WHEN [dbo].[movimientos].codigo LIKE '102%' THEN 'Bancos' WHEN [dbo].[movimientos].codigo LIKE '101%' THEN 'Caja' WHEN [dbo].[movimientos].codigo LIKE '100%' THEN 'Fondo Fijo Caja' WHEN [dbo].[movimientos].codigo LIKE '103%' THEN 'Clientes' WHEN [dbo].[movimientos].codigo LIKE '104%' THEN 'Documentos por Cobrar' WHEN [dbo].[movimientos].codigo LIKE '105%' THEN 'Deudores Diversos' WHEN [dbo].[movimientos].codigo LIKE '106%' THEN 'IVA Acreditable' WHEN [dbo].[movimientos].codigo LIKE '107%' THEN 'Funcionarios y Empleados' WHEN [dbo].[movimientos].codigo LIKE '108%' THEN 'Inventarios' WHEN [dbo].[movimientos].codigo LIKE '109%' THEN 'Anticipo a Proveedores' WHEN [dbo].[movimientos].codigo LIKE '120%' THEN 'Mobiliario y Equipo de oficina' WHEN [dbo].[movimientos].codigo LIKE '121%' THEN 'Depreciación Acumulada de Mob y Eq. oficina' WHEN [dbo].[movimientos].codigo LIKE '122%' THEN 'Equipo de Transporte' WHEN [dbo].[movimientos].codigo LIKE '123%' THEN 'Depreciación Acumulada Equipo Transporte' WHEN [dbo].[movimientos].codigo LIKE '124%' THEN 'Equipo de cómputo' WHEN [dbo].[movimientos].codigo LIKE '125%' THEN 'Depreciación acumulada Eq. cómputo' WHEN [dbo].[movimientos].codigo LIKE '126%' THEN 'Edificios' WHEN [dbo].[movimientos].codigo LIKE '127%' THEN 'Depreciación Acumulada Edificios' WHEN [dbo].[movimientos].codigo LIKE '128%' THEN 'Terrenos' WHEN [dbo].[movimientos].codigo LIKE '129%' THEN 'Equipo de Servicios' WHEN [dbo].[movimientos].codigo LIKE '130%' THEN 'Depreciación acumulada de Eq. de Servicios' WHEN [dbo].[movimientos].codigo LIKE '140%' THEN 'Gastos de Organización' WHEN [dbo].[movimientos].codigo LIKE '141%' THEN 'Gastos de Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '142%' THEN 'Impuestos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '143%' THEN 'Gastos Anticipados' WHEN [dbo].[movimientos].codigo LIKE '144%' THEN 'Deposito en Garantia' WHEN [dbo].[movimientos].codigo LIKE '150%' THEN 'Amortización Gastos Organización' WHEN [dbo].[movimientos].codigo LIKE '151%' THEN 'Amortización Gastos Instalación y Adaptación' WHEN [dbo].[movimientos].codigo LIKE '200%' THEN 'PROVEEDORES' WHEN [dbo].[movimientos].codigo LIKE '201%' THEN 'ACREEDORES DIVERSOS' WHEN [dbo].[movimientos].codigo LIKE '202%' THEN 'IMPUESTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '203%' THEN 'DOCUMENTOS POR PAGAR' WHEN [dbo].[movimientos].codigo LIKE '204%' THEN 'IVA Trasladado' WHEN [dbo].[movimientos].codigo LIKE '205%' THEN 'Anticipos de Clientes' WHEN [dbo].[movimientos].codigo LIKE '206%' THEN 'Sueldos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '207%' THEN 'Gastos por Pagar' WHEN [dbo].[movimientos].codigo LIKE '208%' THEN 'PTU por Pagar' WHEN [dbo].[movimientos].codigo LIKE '220%' THEN 'Acreedores Hipotecarios' WHEN [dbo].[movimientos].codigo LIKE '221%' THEN 'Creditos Bancarios' WHEN [dbo].[movimientos].codigo LIKE '230%' THEN 'Intereses cobrados por adelantado' WHEN [dbo].[movimientos].codigo LIKE '000-030%' THEN 'CAPITAL' WHEN [dbo].[movimientos].codigo LIKE '000-031%' THEN 'Capital Social' WHEN [dbo].[movimientos].codigo LIKE '000-033%' THEN 'Resultado Ejercicios Anteriores' WHEN [dbo].[movimientos].codigo LIKE '000-034%' THEN 'Resultado del Ejercicio' WHEN [dbo].[movimientos].codigo LIKE '000-035%' THEN 'Utilidades Retenidas' ELSE 'Otros' END").fetchall()
    for hola in json:
        print(hola, "este es hola")
    cnxn.commit()
    #cursor.close()
    return json

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
