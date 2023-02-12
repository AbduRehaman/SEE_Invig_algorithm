import see_invig_alloc as s
import matplotlib.pyplot as plt



cursor, connection = s.connect()
query = "delete from has_exam"
cursor.execute(query)
connection.commit()
query = "delete from assigned_classrooms"
cursor.execute(query)
query = "delete from enrolled"
cursor.execute(query)
connection.commit()
query = "update faculty set Invig_count=0"
cursor.execute(query)
connection.commit()
query = "delete from invigilates"
cursor.execute(query)
connection.commit()


possible_exams = s.get_possible_exams(cursor, connection)
for i in possible_exams:
    s.insert_into_has_exam(i[0], i[1], i[2], cursor, connection)
    s.insert_into_enrolled(i[0], i[1], i[2], cursor, connection)

s.assign_students_enrolled_to_enrolled(cursor,connection)
for i in possible_exams:
    s.assign_classrooms(i[2], i[1], i[0], cursor, connection)

groups = s.get_groups(cursor, connection)

classrooms_to_be_assigned = s.get_classrooms_assigned(cursor, connection)

s.group_gets_assigned(classrooms_to_be_assigned, cursor, connection)

query = "select Faculty_ID, Invig_count from FACULTY"
cursor.execute(query)
records = cursor.fetchall()
faculty = []
invig_count = []
for row in records:
    faculty.append(row[0])
    invig_count.append(row[1])
plt.bar(faculty, invig_count)
plt.xlabel("Faculty ID")
plt.ylabel("Invigilator Count")
plt.show()



