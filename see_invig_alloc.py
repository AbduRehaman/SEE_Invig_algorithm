import mysql.connector
import math
import random
import matplotlib.pyplot as plt


import mysql.connector
from mysql.connector import Error
def connect():
    try:
        connection = mysql.connector.connect(    host="localhost",
        database="SEE_INV_withflask_tryingalgo",
        user="root",
        password="root@123")
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            record = cursor.fetchone()
            return cursor,connection

    except Error as e:
        print("Error while connecting to MySQL", e)

def get_possible_exams(cursor, connection):
    query = "select * from EXAM"
    cursor.execute(query)
    records = cursor.fetchall()
    exams = []
    for row in records:
        exams.append(row)
    exams = set(exams)
    exams = list(exams)
    query = "select Subject_ID from SUBJECT"
    cursor.execute(query)
    records = cursor.fetchall()
    subjects = []
    for row in records:
        subjects.append(row)
    subjects = set(subjects)
    subjects = list(subjects)
    possible_exams = []
    for i in exams:
        for j in subjects:
            possible_exams.append([i[0], i[1], j[0]])
    return possible_exams

def insert_into_has_exam(academic_year, exam_type, subject_id,cursor,connection):
    query = "insert into HAS_EXAM(academic_year, exam_type, subject_id) values(%s, %s, %s)"
    cursor.execute(query, (academic_year, exam_type, subject_id))
    connection.commit()

def insert_into_enrolled(academic_year, exam_type, subject_id,cursor,connection):
    query = "insert into ENROLLED(academic_year, exam_type, subject_id) values(%s, %s, %s)"
    cursor.execute(query, (academic_year, exam_type, subject_id))
    connection.commit()

def update_enrolled(subject_id, students_enrolled, exam_type, academic_year,cursor,connection):
    query = "update ENROLLED set students_enrolled = %s where Subject_ID = %s and Exam_Type = %s and Academic_Year = %s"
    cursor.execute(query, (students_enrolled, subject_id, exam_type, academic_year))
    connection.commit()

def insert_into_classroom(classroom_id, capacity, department_id,cursor,connection):
    query = "insert into CLASSROOM values(%s, %s, %s)"
    cursor.execute(query, (classroom_id, capacity, department_id))
    connection.commit()

def get_students_enrolled(subject_id, exam_type, academic_year,cursor,connection):
    query = "select Students_Enrolled from ENROLLED where Subject_ID = %s and Exam_Type = %s and Academic_Year = %s"
    cursor.execute(query, (subject_id, exam_type, academic_year))
    records = cursor.fetchall()
    students_enrolled = records[0][0]
    return students_enrolled

def get_classrooms(cursor,connection):
    query = "select Classroom_ID, Capacity, Dept_ID from CLASSROOM"
    cursor.execute(query)
    records = cursor.fetchall()
    classrooms = []
    for row in records:
        classrooms.append(row)
    return classrooms

def assign_classrooms(subject_id, exam_type, academic_year,cursor,connection):
    students_enrolled = get_students_enrolled(subject_id, exam_type, academic_year,cursor,connection)
    available_classrooms = get_classrooms(cursor,connection)
    used_classrooms = []
    for i in available_classrooms:
        x = random.randint(0, len(available_classrooms)-1)
        if(students_enrolled>0 and available_classrooms[x] not in used_classrooms):
            if(students_enrolled<=available_classrooms[x][1]):
                used_classrooms.append(available_classrooms[x])
                # print(available_classrooms[x][0]+', '+available_classrooms[x][2])
                students_enrolled = 0
            else:
                used_classrooms.append(available_classrooms[x])
                # print(available_classrooms[x][0]+', '+available_classrooms[x][2])
                students_enrolled = students_enrolled - available_classrooms[x][1]
    t = len(used_classrooms)
    query = "update HAS_EXAM set required_invigilators = %s where Subject_ID = %s and Exam_Type = %s and Academic_Year = %s"
    cursor.execute(query, (t, subject_id, exam_type, academic_year))
    connection.commit()
    for i in used_classrooms:
        query = "insert into assigned_classrooms values(%s, %s, %s, %s, %s)"
        cursor.execute(query, (i[0], subject_id, exam_type, academic_year, i[2]))

def get_groups(cursor,connection):
    query = "select Group_ID, Dept_ID, Invig_count from FACULTY"
    cursor.execute(query)
    records = cursor.fetchall()
    answer = []
    for row in records:
        answer.append(row)
    answer = set(answer)
    answer = list(answer)
    return answer

def get_invig_count(faculty_id, department_id,cursor,connection):
    query = "select Invig_count from FACULTY where Faculty_ID = %s and Dept_ID = %s"
    cursor.execute(query, (faculty_id, department_id))
    records = cursor.fetchall()
    invig_count = records[0][0]
    return invig_count

def get_faculties_in_group(group_id, department_id,cursor,connection):
    query = "select Faculty_ID from FACULTY where Group_ID = %s and Dept_ID = %s"
    cursor.execute(query, (group_id, department_id))
    records = cursor.fetchall()
    faculties = []
    for row in records:
        faculties.append(row[0])
    return faculties

def assign_faculty_classroom(faculty_id, academic_year, exam_type, classroom_id, department_id, subject_id,cursor,connection):
    query = "insert into invigilates values(%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (faculty_id, academic_year, exam_type, classroom_id, department_id, subject_id))
    connection.commit()

def get_classrooms_assigned(cursor,connection):
    query = "select * from assigned_classrooms"
    cursor.execute(query)
    records = cursor.fetchall()
    classrooms = []
    for row in records:
        classrooms.append(row)
    return classrooms

def increment_invig_count(faculty_id, department_id,cursor,connection):
    query = "update FACULTY set Invig_count = Invig_count + 1 where Faculty_ID = %s and Dept_ID = %s"
    cursor.execute(query, (faculty_id,department_id))
    connection.commit()

def group_gets_assigned(classrooms,cursor,connection):
    y = random.sample(range(0,len(classrooms)), len(classrooms)-1)
    while(len(y)!=0):
        groups = get_groups(cursor,connection)
        groups.sort(key = lambda x: x[2])
        x = random.randint(0,3)
        faculties_group = get_faculties_in_group(groups[x][0], groups[x][1],cursor,connection)
        for i in faculties_group:
            # print(i)
            if len(y)==0:
                break
            t = y.pop()
            # print(classrooms[t][3])
            # print(classrooms[t][2])
            # print(classrooms[t][0])
            # print(classrooms[t][4])
            # print(groups[x][1])
            assign_faculty_classroom(i, classrooms[t][3], classrooms[t][2], classrooms[t][0], classrooms[t][4], classrooms[t][1],cursor,connection)
            increment_invig_count(i, groups[x][1],cursor,connection)

def assign_students_enrolled_to_enrolled(cursor,connection):
    query = "update enrolled set students_enrolled = (select count(*) from student where student.exam_type = enrolled.exam_type and student.subject_id = enrolled.subject_id);"
    cursor.execute(query)
    connection.commit()