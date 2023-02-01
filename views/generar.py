from flask import render_template, send_file, request, redirect
import io, zipfile, time

from utils.coneccion import login, datos_estudiantes
from utils.limpia import limpia
from utils.constanciagen import createPDF

import datetime 

from data import getDbData
from secret import user, password
from secret import login_required

data_db = getDbData()

dias_fechas = {
    0: 'lunes',
    1: 'martes',
    2: 'miércoles',
    3: 'jueves',
    4: 'viernes',
    5: 'sábado',
    6: 'domingo'
}

meses = {
    '01': 'enero',
    '02': 'febrero',
    '03': 'marzo',
    '04': 'abril',
    '05': 'mayo',
    '06': 'junio',
    '07': 'julio',
    '08': 'agosto',
    '09': 'septiembre',
    '10': 'octubre',
    '11': 'noviembre',
    '12': 'diciembre'
}
programas_no_periodos = {
    'DOCTORADO EN ENERGÍA': 8,
    'DOCTORADO EN FÍSICA DE LOS MATERIALES': 8,
    'DOCTORADO EN CIENCIAS FISICOMATEMÁTICAS': 8,
    'MAESTRÍA EN CIENCIAS FISICOMATEMÁTICAS': 5,
}


@login_required
def index():
    data_db = getDbData()
    return render_template(
        'index.html',
        periodos=data_db['periodos'],
    )

@login_required
def generar_constancias():
    global data_db
    data = request.form
    fecha = data['fecha_actual']
    no_dia = datetime.datetime.strptime(fecha,"%Y-%m-%d" ).weekday()
    fecha_actual = f'{dias_fechas[no_dia]} {fecha[-2:]} de {meses[fecha[5:7]]} del {fecha[:4]}' 
    
    semestre_actual = data['semestre_actual']
    tipo_constancia = data['tipo_constancia']

    boletas = data['boletas'].replace(' ', '').split(',')
    if not boletas: 
        return redirect('/')

    data_db = getDbData() #Consulta a la DB
    alumnos = datos_estudiantes(
        boletas, 
        login(user, password), 
        data_db['periodos']
    )

    datos = limpia(alumnos, tipo_constancia, semestre_actual)
    bytes_pdfs = [
        createPDF(
                dato, 
                data_db[tipo_constancia]['contenido'], 
                fecha_actual, 
                programas_no_periodos[dato['nombre_programa']], 
                semestre_actual,
                data_db['vars']['nombre_signatario'],
                data_db['vars']['puesto_signatario'],
                data_db['vars']['periodo_actual_inicio_fecha'],
                data_db['vars']['periodo_actual_fin_fecha'],
                data_db['vars']['fondo'],
            ) for dato in datos 
    ]

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for i, individualFile, dato in zip(range(len(bytes_pdfs)), bytes_pdfs, datos):
            data_zip = zipfile.ZipInfo(f'{dato["registro"]}_{tipo_constancia}_{semestre_actual}.pdf')
            data_zip.date_time = time.localtime(time.time())[:6]
            data_zip.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data_zip, individualFile)
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename=f'Constancias_{tipo_constancia}_{semestre_actual.replace(" ","")}.zip', as_attachment=True)