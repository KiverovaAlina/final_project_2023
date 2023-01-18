import static.desc
from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.doctor_model import get_speciality

@app.route('/doctor', methods=['get', 'post'])
def doctor():
    conn = get_db_connection()
    df_speciality = get_speciality(conn)

    if request.values.get('speciality'):
        f = 2
        doctor_id = int(request.values.get('speciality'))
        image = '/static/images/'+str(doctor_id)+'.jpg'
        df_desc_dict = static.desc.spec_dict[doctor_id]
        session['doctor_id'] = doctor_id
    elif request.form.get('clear'):
        f = 1
        df_desc_dict = {}
        session['doctor_id'] = 1
        image = None
    else:
        f = 1
        df_desc_dict = {}
        session['doctor_id'] = 1
        image = None



    html = render_template(
        'doctor.html',
        discription = df_desc_dict,
        combo_box=df_speciality,
        image= image,
        doctor_id = session['doctor_id'],
        flag = f,
        len=len


    )
    return html
