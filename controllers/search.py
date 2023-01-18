from app import app
from flask import render_template, request
from utils import get_db_connection
from models.search_model import get_doctor, get_symptom, get_diagnosis, get_type, get_app


@app.route('/search', methods=['GET', 'POST'])
def search():
    # устанавливаем соединение с базой данных
    conn = get_db_connection()

    # выполняем запросы к БД
    df_doctor = get_doctor(conn)
    df_symptom = get_symptom(conn)
    df_diagnosis = get_diagnosis(conn)
    df_type = get_type(conn)

    if request.form.get('clear'):
        doctors = []
        diagnoses = []
        symptoms = []
        types = []
    else:
        doctors = request.form.getlist('doctors')
        diagnoses = request.form.getlist('diagnoses')
        symptoms = request.form.getlist('symptoms')
        types = request.form.getlist('types')

    df_app = get_app(conn, types, doctors, symptoms, diagnoses)

    # выводим форму
    html = render_template(
        'search.html',
        sections=['types', 'doctors', 'symptoms', 'diagnoses'],
        all_data=[df_type, df_doctor, df_symptom, df_diagnosis],
        all_choices=[ types, doctors, symptoms, diagnoses],
        appointments=df_app,
        types = types,
        doctor_list=doctors,
        symptoms=symptoms,
        diagnoses=diagnoses,
        len=len,
        zip=zip,

    )
    return html
