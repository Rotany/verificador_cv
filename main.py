from PyPDF2 import PdfReader
from flask import Flask , request, jsonify

app = Flask(__name__)


def verificar_apto(archivo_pdf, archivo_palabras_clave):
    reader = PdfReader(archivo_pdf)
    
    page = reader.pages[0]
    text = page.extract_text().lower()
    verificador = {
        'palabras_encontradas': [],
        'palabras_faltantes': [],
        'es_apto': True
    }

    with open(archivo_palabras_clave,'r') as stop_words: 
        
        palabras_clave = [linea.strip().lower() for linea in stop_words]

    for palabra_clave in palabras_clave:
        
        if palabra_clave in text:
            verificador['palabras_encontradas'].append(palabra_clave)
        else:
            verificador['palabras_faltantes'].append(palabra_clave)
    
    es_apto = len(verificador['palabras_encontradas'])== len(palabras_clave)
    verificador['es_apto'] = es_apto 
    return(verificador) 

# verificar = verificar_apto('data/curriculum.pdf','data/palabras_clave.txt' )

if __name__ == '__main__':
    app.run()
