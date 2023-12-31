from PyPDF2 import PdfReader
from flask import Flask , request, jsonify
import os

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

    palabras_clave = archivo_palabras_clave.split(',')
    palabras_clave = [palabra.strip().lower() for palabra in palabras_clave]

    for palabra_clave in palabras_clave:
        
        if palabra_clave in text:
            verificador['palabras_encontradas'].append(palabra_clave)
        else:
            verificador['palabras_faltantes'].append(palabra_clave)
    
    es_apto = len(verificador['palabras_encontradas'])== len(palabras_clave)
    verificador['es_apto'] = es_apto 
    return(verificador) 

# verificar = verificar_apto('data/curriculum.pdf','data/palabras_clave.txt' )


@app.route('/cv-analyzer',methods = ['POST'])
def verificador_cv():
    archivo_pdf = request.files['pdf']
    palabras_clave = request.form['palabras_clave']
    verificar = verificar_apto(archivo_pdf, palabras_clave)
    return(jsonify(verificar))



port = int(os.environ.get('PORT', 33507))

app.run(debug=True, port=port)


