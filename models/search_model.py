import pandas as pd
def get_type(conn):
    return pd.read_sql('''
        SELECT type, 
        count(appointment_id) 
        FROM type t
        INNER JOIN appointment a on t.type_id = a.type_id
        GROUP BY type''', conn)


def get_diagnosis(conn):
    return pd.read_sql('''
        SELECT diagnosis, 
        count(appointment_id) 
        FROM diagnosis d
        INNER JOIN appointment a on d.diagnosis_id = a.diagnosis_id
        GROUP BY diagnosis''', conn)


def get_doctor(conn):
    return pd.read_sql('''
        SELECT speciality, 
        count(appointment_id)
        FROM doctor d
        INNER JOIN appointment a on d.doctor_id = a.doctor_id
        GROUP BY speciality''', conn)


def get_symptom(conn):
    return pd.read_sql('''
        SELECT symptom, 
        count(a.appointment_id) 
        FROM symptom s
        INNER JOIN app_symptom on s.symptom_id = app_symptom.symptom_id
        INNER JOIN appointment a on a.appointment_id = app_symptom.appointment_id
        GROUP BY symptom''', conn)


def get_app(conn, types, doctors, symptoms, diagnoses):
    return pd.read_sql(f'''
WITH apps_query AS (SELECT a.appointment_id,
                            type Тип_приема,
                            speciality Доктор,
              
                            diagnosis  Диагноз
                            
                     FROM appointment a
                              INNER JOIN app_symptom on a.appointment_id = app_symptom.appointment_id
                              INNER JOIN type t on t.type_id = a.type_id
                                AND (type IN ({str(types).strip('[]')}) OR {not types})
                              INNER JOIN symptom s on s.symptom_id = app_symptom.symptom_id
                                AND (symptom IN ({str(symptoms).strip('[]')}) OR {not symptoms})
                              INNER JOIN doctor d on d.doctor_id = a.doctor_id
                                AND (speciality IN ({str(doctors).strip('[]')}) OR {not doctors})
                              INNER JOIN diagnosis on diagnosis.diagnosis_id = a.diagnosis_id
                                AND (diagnosis IN ({str(diagnoses).strip('[]')}) OR {not diagnoses})
                     GROUP BY a.appointment_id)
SELECT apps_query.appointment_id,
        Тип_приема,
       Доктор,
       Диагноз,
       group_concat(symptom) Симптом
FROM apps_query
        INNER JOIN app_symptom on apps_query.appointment_id = app_symptom.appointment_id
         INNER JOIN symptom s on s.symptom_id = app_symptom.symptom_id
        
GROUP BY apps_query.appointment_id
''', conn)
