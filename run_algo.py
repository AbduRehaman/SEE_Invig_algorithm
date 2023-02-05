import see_invig_alloc as s
import random
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt

cursor, connection = s.connect()
possible_exams = s.get_possible_exams(cursor, connection)
for i in possible_exams:
    s.insert_into_has_exam(i[0], i[1], i[2], cursor, connection)
    #For initial connect to database, uncomment the below line, and fill the students enrolled value
    # s.insert_into_enrolled(i[0], i[1], i[2], cursor, connection)

for i in possible_exams:
    s.assign_classrooms(i[2], i[1], i[0], cursor, connection)

groups = s.get_groups(cursor, connection)

classrooms_to_be_assigned = s.get_classrooms_assigned(cursor, connection)

s.group_gets_assigned(classrooms_to_be_assigned, cursor, connection)

