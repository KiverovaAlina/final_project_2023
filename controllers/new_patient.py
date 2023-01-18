from app import app
from flask import render_template, request, session


@app.route('/new_patient', methods=['get'])
def new_patient():
    # выводим форму
    html = render_template(
        'new_patient.html',
    )
    return html
