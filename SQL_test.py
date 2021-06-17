import sqlite3

def show_sql():
    cur.execute('''SELECT * FROM people''')
    res = cur.fetchall()
    print(res)


def add_people(id, name, surname, age, alone=0):
    cur.executemany('INSERT INTO people (id, name, surname, age, alone) VALUES (?,?,?,?,?)', [(id, name, surname, age, alone)])
    conn.commit()


def greater(p1, p2):
    cur.execute('''SELECT age FROM people WHERE surname = (?) OR surname = (?)''', (p1, p2))
    a, b = cur.fetchall()
    li = [a, b]
    for i in li:
        i = i[0]
    print(a<b)


def select_data_of(names, data="age"):
    select = []
    for name in names:
        cur.execute(f'''SELECT [{data}] FROM people WHERE surname = (?)''', (name, ))
        select.append(cur.fetchall()[0])
    return select


with sqlite3.connect('test.s3db') as conn:
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS people''')
    cur.execute('''CREATE TABLE IF NOT EXISTS people
                    (id INTEGER,
                    name TEXT,
                    surname TEXT,
                    age INTEGER,
                    alone INTEGER DEFAULT 0);''')
    
    add_people(1, 'SMITH', 'James', 27)
    add_people(2, 'JOHNSON','Mike', 34)
    n = 'James'
    res = cur.execute('''SELECT age + (?) FROM people WHERE surname = (?)''', (10, n))
    res = cur.fetchall()[0][0]
    print(res)
    res = cur.execute('''SELECT age, alone FROM people WHERE surname = (?)''', ("Mike", ))
    res = cur.fetchall()
    print(res[0][1])
