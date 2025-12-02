import subprocess
import os

comandos = """
list volume
exit
"""

script_file = r"C:\Users\Jefferson\desarrollo python\hello_python\Python\Projects\DiskFix\script_diskpart.txt"
with open (script_file, "w") as f:
  f.write(comandos)

try:
  print("Ejecutando diskpart ...")
  proceso = subprocess.run(
    ["diskpart" , "/s",script_file],
      capture_output=True, text=True)

  if proceso.returncode == 0:
    print ("--- Exito ---")
    print(proceso.stdout)
  else:
    print("--- Error ---")
    print(proceso.stderr)
finally:
  print("Ejecutado el comando correctamente")