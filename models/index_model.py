import pandas


def get_patient(conn):
    return pandas.read_sql(
        '''SELECT * FROM patient
''', conn)


def get_app_patient(conn, patient_id):
    # выбираем и выводим записи о том, какие книги брал читатель
    return pandas.read_sql('''WITH get_symptoms(appointment_id, symptoms)
         AS (SELECT appointment_id, GROUP_CONCAT(symptom)
             FROM symptom
                      JOIN app_symptom USING (symptom_id)
             GROUP BY appointment_id)
SELECT 
        type AS Тип_приема,
        date AS Дата,
        speciality AS Доктор,
       diagnosis  AS Диагноз,
       symptoms AS Симптомы,
       app_patient_id
FROM patient
         JOIN app_patient USING (patient_id)
         JOIN appointment USING (appointment_id)
         JOIN doctor USING (doctor_id)
         JOIN type USING (type_id)
         JOIN diagnosis USING (diagnosis_id)
         JOIN get_symptoms USING (appointment_id)
WHERE patient.patient_id = :id
ORDER BY 3
         ''', conn, params={"id": patient_id})


# для обработки данных о новом пациенте
def get_new_patient(conn, new_patient):
    cur = conn.cursor()

    cur.execute('''
INSERT INTO patient(patient_name) VALUES (:new_patient)
    ''', {"new_patient": new_patient})

    conn.commit()

    return cur.lastrowid


# для обработки данных о новом приеме
def borrow_app(conn, appointment_id, patient_id):
    cur = conn.cursor()

    cur.executescript(f'''
    INSERT INTO app_patient(appointment_id, patient_id, date) VALUES ({appointment_id},{patient_id}, date('now'));

    

    ''')

    return conn.commit()

# для обработки данных об закрытии приема
def close_app(con, app_patient_id):
    cur = con.cursor()

    appointment_id = pandas.read_sql(f'''
    SELECT appointment_id FROM app_patient WHERE app_patient_id = {app_patient_id}
    ''', con).values[0][0]

    
    return con.commit()


"""
# Увеличить количество экземпляров книг в таблице book и указать текущую дату как дату сдачи книги в таблице book_reader
def return_book(conn, book_reader_id):
    cur = conn.cursor()

    book_id = pandas.read_sql(f'''
SELECT book_id FROM book_reader WHERE book_reader_id = {book_reader_id}
    ''', conn).values[0][0]

    cur.executescript(f'''
UPDATE book
SET available_numbers = available_numbers + 1
WHERE book_id = {book_id};

UPDATE book_reader
SET return_date = date('now')
WHERE book_reader_id = {book_reader_id}
    ''')

    return conn.commit()
"""