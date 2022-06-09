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

def verEmpresasPorfi(idEmpresa, idUsuario):
    params = (idEmpresa, idUsuario)
    cursor = init_db()
    cursor.execute("insert into [dbo].[usuario_empresa] values (?,?)", params)
    cnxn.commit()
    cursor.close()
