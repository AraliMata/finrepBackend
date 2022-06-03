from datetime import date
import pyodbc
import logging

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


def mesesDispoibles(idEmpresa):
    storedProc = {"meses": "EXEC dbo.mesesDisponibles @empresaID = ?" }
    params = (idEmpresa)
    cursor = init_db()
    data = []
    datos = {}
    for tipo in storedProc:
        resultado = cursor.execute(storedProc[tipo],params)
        rows = cursor.fetchall()
        for row in rows:
            data.append(list(row)[0])
        datos[tipo] = data
        data = []
    
    print(datos)

    return datos
