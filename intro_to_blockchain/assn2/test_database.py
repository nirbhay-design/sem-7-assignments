import sqlite3

con = sqlite3.connect("dbb.sqlite3")

cursor = con.cursor()

try:
    cursor.execute(
        """create table database (
            id varchar(256),
            name varchar,
            surname varchar
        )"""
    )
except:
    print("table already exists")

response = cursor.execute('insert into database (id, name, surname) values ("2", "nirbhay", "sharma")')
con.commit()

response = cursor.execute('insert into database (id, name, surname) values ("3", "nirbha", "sarma")')
con.commit()

response = cursor.execute('insert into database (id, name, surname) values ("4", "nirbh", "shar")')
con.commit()

res = cursor.execute("select id from database")

print(res.fetchall())

res = cursor.execute("select count(*) from database")
print(res.fetchall())

con.close()




# from ecdsa import SingingKey
# s = '27167c645228076e97b95239bb085ab2be1aeeed38d7d971'
# byte = bytes()
# byte_key = byte.fromhex(s)
# new_key = SigningKey.from_string(byte_key)
