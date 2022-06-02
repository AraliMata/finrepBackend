import pyodbc
import pandas as pd
from datetime import datetime
import numpy as np

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

def readXlsxFile(request,idEmpresa):
    print(request.FILES['movimientos'])
    df = pd.read_excel(request.FILES['movimientos'])
    print (df)
    df_listo = fix_df(df, request,idEmpresa)
    return df_listo


def insertInDatabase(df,idEmpresa):
    cursor = init_db()
    print("HOLA MAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(catalogo)
    print (catalogo.loc[lambda catalogo: catalogo['nivel'] == 1])
    # print (catalogo.loc[catalogo['nivel'] == '1'])
    for row in catalogo.loc[lambda catalogo: catalogo['nivel'] == 1].iterrows():
        cur = row[1]
        print(cur['codigo'])
        # print(row.nivel)
        cursor.execute("BEGIN IF NOT EXISTS (SELECT * FROM dbo.codigos_agrupadores WHERE codigo = ? AND idEmpresa_id = ?) BEGIN INSERT INTO dbo.codigos_agrupadores VALUES (?, ?, ?, ?) END END", cur['codigo'], idEmpresa, cur['codigo'], cur['tipo'], idEmpresa, cur['nombre'])
        
    for row in catalogo.loc[lambda catalogo: catalogo['nivel'] == 2].iterrows():
        cur = row[1]
        cursor.execute("BEGIN IF NOT EXISTS (SELECT * FROM dbo.codigos_agrupadores WHERE codigo = ? AND idEmpresa_id = ?) BEGIN INSERT INTO dbo.codigos_agrupadores VALUES (?, ?, ?, ?) END END", cur['codigo'], idEmpresa, cur['codigo'], cur['tipo'], idEmpresa, cur['nombre'])
        
    for index, row in df.iterrows():
        # print(row)
        # print(row.id_empresa," ", row.codigo," ", row.nombre," ", row.concepto," ", row.referencia," ", float(row.saldo_inicial)," ", float(row.cargos)," ", float(row.abonos)," ", row.fecha)
        cursor.execute("INSERT INTO dbo.movimientos (idEmpresa_id,codigo,nombre,concepto,referencia,saldoInicial,cargos,abonos,fecha,codigoAgrupador,ingresoEgreso,nombreAgrupador,tipo) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",row.id_empresa,row.codigo,row.nombre,row.concepto,row.referencia,float(row.saldo_inicial),float(row.cargos),float(row.abonos),row.fecha,row.codigo_agrupador,row.tipo,row.nombre_grupo,row.APC)
    cnxn.commit()
    cursor.close()

def es_agrupador(code):
    serie = catalogo.loc[catalogo['codigo'] == code]
    nivel = serie.loc[catalogo['nivel'] == 3]
    #print(nivel)
    if nivel.size > 0:
        tipo = nivel.iat[0, 3]
        return (True, tipo)
    else:
        tipo1 = serie.loc[catalogo['tipo'] == 'H Resultados Acreedora']
        tipo2 = serie.loc[catalogo['tipo'] == 'G Resultados Deudora']
        tipo3 = serie.loc[catalogo['tipo'] == 'F Capital Acreedora']
        
        if tipo1.size > 0:
            tipo = tipo1.iat[0, 3]
            agrupador = tipo1.iat[0, 2]
            return (True, tipo, agrupador)
        elif tipo2.size > 0:
            tipo = tipo2.iat[0, 3]
            agrupador = tipo2.iat[0, 2]
            return (True, tipo, agrupador)
        elif tipo3.size > 0:
            tipo = tipo3.iat[0, 3]
            return (True, tipo)
        else:
            return (False, 0)

def is_valid(row):
    if (row[1] != "" and pd.isna(row[2])==False):
        return True
    else:
        return False

def format_date(date):
    datetimeobject = datetime.strptime(date, '%d/%b/%Y')
    new_date = datetimeobject.strftime('%Y-%m-%d')
    return new_date

def fix_df(df, request,idEmpresa):
    global catalogo
    catalogo = pd.read_excel(request.FILES['catalogo'])
    print(catalogo)

    df.columns = ['fecha', 'tipo', 'numero', 'concepto', 'referencia', 'cargos', 'abonos', 'saldo']
    catalogo.columns = ['nivel', 'codigo', 'nombre', 'tipo', 'afectable', 'dig', 'edo', 'moneda', 'seg', 'rubro', 'agrupador']


    column_names = ['id_empresa', 'codigo', 'codigo_agrupador', 'nombre', 'nombre_grupo', 'tipo', 'APC', 'fecha', 'concepto', 'referencia', 'cargos', 'abonos', 'saldo', 'saldo_inicial']
    new_df = pd.DataFrame(columns = column_names)

    current_code = ""
    current_name = ""
    current_agrupador = ""
    current_saldoi = 0
    current_nombreG = ""
    current_APC = ""      
        
    count = 0
    for row in df.itertuples():
        if count > 6:        
            if (row[7] == 'Saldo inicial :'):
                agrupador = es_agrupador(row[1])
                if(agrupador[0]):
                    current_agrupador = row[1]
                    current_nombreG = row[2]
                    current_APC = agrupador[1]
                current_code = row[1]
                current_name = row[2]
                current_saldoi = row[8]
                fecha_inicial = datetime(2016, 6, 1)
                temp_df = {'id_empresa': idEmpresa, 'codigo': current_code, 'codigo_agrupador': current_agrupador, 'nombre': current_name,'nombre_grupo': current_nombreG,'tipo': "", 'APC': current_APC, 'fecha': '2016-06-01', 'concepto': '', 'referencia': '', 'cargos': 0.0, 'abonos': 0.0, 'saldo': 0.0, 'saldo_inicial': current_saldoi}
                new_df = new_df.append(temp_df, ignore_index=True)

            elif (is_valid(row)):
                new_date = format_date(row[1])

                if (pd.isna(row[6])):
                        cargos = 0.0
                else:
                    cargos = row[6]

                if (pd.isna(row[7])):
                    abonos = 0.0
                else:
                    abonos = row[7]

                if (pd.isna(row[7])):
                    saldo = 0.0
                else:
                    saldo = row[8]

                temp_df = {'id_empresa': idEmpresa, 'codigo': current_code, 'codigo_agrupador': current_agrupador, 'nombre': current_name,'nombre_grupo': current_nombreG,'tipo': row[2],'APC': current_APC, 'fecha': new_date, 'concepto': row[4], 'referencia': row[5], 'cargos': cargos, 'abonos': abonos, 'saldo': saldo, 'saldo_inicial': current_saldoi}
                new_df = new_df.append(temp_df, ignore_index=True)

        else:
            count = count + 1
    new_df = new_df.replace(r'^\s*$', np.NaN, regex=True)
    new_df = new_df.replace(np.nan, 'vacio', regex=True)
    print(new_df.head)
    return new_df