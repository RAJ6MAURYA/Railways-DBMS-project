import psycopg2 as pg
#connection is established
con = pg.connect(host = 'localhost',
                database='Railway',
                user='postgres',
                password='raj',
                port=5432)
cur = con.cursor()
#curser is created 
cur.close()
con.close()

print("Welcome to the DataBase Managemet System")
print("Enter the operation you want to do",end="\n")
print("1.Insert a value\n2.View\n.3.Delete\n4.Update")