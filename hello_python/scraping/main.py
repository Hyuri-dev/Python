import requests
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings('ignore', category=requests.exceptions.RequestsWarning)

r = requests.get('https://www.bcv.org.ve/', verify=False)

clase = 'col-sm-6 col-xs-6 centrado'


soup = BeautifulSoup(r.text, 'lxml')

def obtener_bcv():
    """
    Funcion para obtener el valor del dolar bcv al dia actual haciendo scraping
    """
    divs_tasas = soup.find_all('div', class_= clase) #find_all para buscar todos los divs que contienen las tasas cambiarias
    
    tasa_bcv = None #iniciamos una variable none, esta nos servira para poder manejar la tasa una vez encontrada
    
    if divs_tasas:
        print(f"Se encontraron {len(divs_tasas)} elementos <div> con la clase especificada")
        
        for div in divs_tasas:
            etiqueta_strong = div.find('strong') #buscamos la etiqueta strong que contiene los valores
            
            if etiqueta_strong:
              ultimo_valor = divs_tasas[-1] #Buscamos el valor que queremos
              tasa_bcv = ultimo_valor.get_text(strip=True)
              tasa_formateada = tasa_bcv.replace("," , ".")
              tasa_bcv = float(tasa_formateada)
              print(f"Valor encontrado: {tasa_bcv}")
              return tasa_bcv
                
            else:
                print("Una de las etiquetas <div> no contenia la etiqueta <strong>")
    else:
        print(f"No se encontraron elementos <div> con la clase {clase} ")
        
tasa_actual = obtener_bcv()
print(f"Tasa del dia de hoy: {tasa_actual}")






