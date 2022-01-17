import psycopg2 as pg
#connection is established
con = pg.connect(host='localhost',
                 database='Railway',
                 user='postgres',
                 password='raj',
                 port=5432)
cur = con.cursor()
#curser is created


def View_Reservation():
    PNR = input("Enter the PNR \n")
    string = "Select * from passengers where PNR = "+PNR
    cur.execute(string)
    out = cur.fetchall()
    l = ["PNR", "NAME", "JOURNEY DATE", "TRIAN NUMBER", "STATUS"]
    for i in range(len(l)):
        print(l[i], " :", out[0][i], end="\t")


print("Welcome to the DataBase Managemet System")
print("Enter the operation you want to do", end="\n")
print("1.Related to Reservation\n2.Availability of Trains\n3.")
ch = int(input())
if(ch == 1):
    print("1.View the Reservation Status\n2.Make a new Reservation\n3.Cancel the Reservation")
    Rch = int(input())
    View_Reservation()
if(ch == 2):
    pass
cur.close()
con.close()
