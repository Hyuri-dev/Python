import psutil as ps

particiones = ps.disk_partitions()
estadisticas = ps.disk_usage('/')

# el valor de las estadisticas las da en bytes si se quiere saber cuantos gb son hay que hacer una transformación
# 1Gb = 1073741824Bytes

print(estadisticas)