from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_patient, get_app_patient, get_new_patient, borrow_app 
#close_app


@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()

    # нажата кнопка Найти
    if request.values.get('patient'):
        patient_id = int(request.values.get('patient'))
        session['patient_id'] = patient_id

    # нажата кнопка "Закрыть прием"
    #elif request.values.get('close_app_patient_id'):
    #    app_patient_id = int(request.values.get('close_app_patient_id'))
    #    close_app(conn, app_patient_id)

    # нажата кнопка "Добавить" со страницы Новый пациент
    elif request.values.get('new_patient'):
        new_patient = request.values.get('new_patient')
        #new_gender = request.values.get('new_gender'), 
        #new_snils = request.values.get('new_snils'), 
        #new_date_birth = request.values.get('new_date_birth'), 
        #new_address = request.values.get('new_address')
        #session['patient_id'] = get_new_patient(conn, new_patient, new_gender, new_snils, new_date_birth, new_address)
        session['patient_id'] = get_new_patient(conn, new_patient)

    # нажата кнопка "Выбрать" со страницы Поиск
    elif request.values.get('appointment'):
        appointment_id = int(request.values.get('appointment'))
        borrow_app(conn, appointment_id, session['patient_id'])

    # нажата кнопка "Не выбирать прием"
    elif request.values.get('noselect'):
        a=1
        
    # вошли первый раз
    else:
        session['patient_id'] = 1

    df_patient = get_patient(conn)
    df_app_patient = get_app_patient(conn, session['patient_id'])

    # выводим форму
    html = render_template(
        'index.html',
        patient_id=session['patient_id'],
        combo_box=df_patient,
        app_patient=df_app_patient,
        len=len
    )
    return html
