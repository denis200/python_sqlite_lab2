import sqlite3
import codecs
try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite")



    cursor.execute(""" CREATE TABLE IF NOT EXISTS groups(
                                                id integer PRIMARY KEY,
                                                facultet VARCHAR(50) NOT NULL,
                                                code VARCHAR(50),
                                                group_number INTEGER
                                            ); """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS student (
                                            id integer PRIMARY KEY,
                                            group_id integer,
                                            last_name VARCHAR(50),
                                            first_name VARCHAR(50),
                                            middle_name VARCHAR(50),
                                            military_responsability BOOLEAN,
                                            FOREIGN KEY (group_id) REFERENCES groups(id)
                                        ); """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS marks (
                                            id integer PRIMARY KEY,
                                            mark integer NOT NULL,
                                            subject VARCHAR(50),
                                            student_id integer NOT NULL,
                                            FOREIGN KEY (student_id) REFERENCES student(id)
                                        ); """)
    print("Подсчитать число групп определенной специальности")
    print(cursor.execute("""SELECT facultet as "Факультет",count(*) as "Количество групп данной специальности" FROM groups group by facultet""").fetchall())
    print("Найти оценку определенного студента по заданному предмету.")
    print(cursor.execute("""select * from marks where subject like "Математика" and student_id=2""").fetchall())
    print("Найти группу, которая сдала больше всего предметов в сессию.")
    print(cursor.execute("""select s.group_id , count(mark)
from marks m
inner join student s on s.id = m.student_id
inner join groups g on g.group_number = s.group_id
where mark >= 25 GROUP by s.group_id
order by count(mark) desc LIMIT 1""").fetchall())
    print("Найти всех студентов, имеющих задолженности")
    print(cursor.execute("""select m.student_id "id", s.last_name "Фамилия",s.first_name "Имя" from marks as m INNER JOIN student as s ON m.student_id = s.id where m.mark < 25""").fetchall())
    print("Подсчитать число студентов, обучающихся на военной кафедре. ")
    print(cursor.execute("""select count(military_responsability) "Военная кафедра" from student where military_responsability = 1""").fetchall())

    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
