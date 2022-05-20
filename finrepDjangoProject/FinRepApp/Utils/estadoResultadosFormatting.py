def valoresIngresos(ingresos, datos, totalIngresos):
    for ingreso in datos:
        periodo = ingreso[1]
        porcentaje = ingreso[1] * 100 / totalIngresos
        ingresos.append([ingreso[2], periodo, porcentaje, periodo, porcentaje])


def valoresEgresos(datos, clasificaciones, totalIngresos):
    for egreso in datos:
        periodo = round(egreso[1], 2)
        porcentaje = round(egreso[1] * 100 / totalIngresos, 2)

        for clasificacion in clasificaciones:
            if egreso[0][0:3] == clasificacion[0][0:3]: 
                clasificacion[3].append([egreso[2], periodo, porcentaje, periodo, porcentaje])
                clasificacion[2] += periodo
    
        #egresos.append([egreso[2], periodo, porcentaje, periodo, porcentaje])

def crearClasificaciones(codigos):
    clasificaciones = []
    for codigo in codigos:
        clasificaciones.append([codigo[1], codigo[4], 0, []])
        codigo.append(False)
    
    return clasificaciones


def agregarEgresos(estadoResultados, clasificaciones, totalIngresos):
    for clasificacion in clasificaciones:
        periodo = round(clasificacion[2], 2)
        porcentaje = round(periodo * 100 / totalIngresos, 2)
        if(periodo != 0):
            estadoResultados['egresos'].append([clasificacion[1], 0,0,0,0])

            for elem in clasificacion[3]:
                estadoResultados['egresos'].append(elem)

            estadoResultados['egresos'].append(['Total '+clasificacion[1], periodo, porcentaje, periodo, porcentaje])

def getUtilidad(datos):
    movimientos = datos['movimientos']

    totalIngresos = sum(list(zip(*movimientos['ingresos']))[1])
    totalEgresos = sum(list(zip(*movimientos['egresos']))[1])

    periodo = round(totalIngresos - totalIngresos, 2)
    porcentaje = round(periodo * 100 / totalIngresos, 2);
    return [periodo, porcentaje, periodo, porcentaje]

def generarResponseEstadoResultados(datos):
    movimientos = datos['movimientos']
    codigos = datos['codes']
    estadoResultados = {'ingresos': [], 'egresos': []}
    totalIngresos = sum(list(zip(*movimientos['ingresos']))[1])
    totalEgresos = sum(list(zip(*movimientos['egresos']))[1])
    clasificaciones = crearClasificaciones(codigos)

    valoresIngresos(estadoResultados['ingresos'], movimientos['ingresos'], totalIngresos)
    valoresEgresos(movimientos['egresos'], clasificaciones, totalIngresos)
    agregarEgresos(estadoResultados, clasificaciones, totalIngresos)

    estadoResultados['ingresos'].append(['Total Ingresos', round(totalIngresos, 2), 100, round(totalIngresos, 2), 100])
    estadoResultados['egresos'].append(['Total Egresos', round(totalEgresos, 2), round(totalEgresos * 100 / totalIngresos, 2), round(totalEgresos, 2), round(totalEgresos * 100 / totalIngresos, 2)])
    estadoResultados['egresos'].append(['Utilidad (o Pérdida)'] + getUtilidad(datos))

    return estadoResultados
  