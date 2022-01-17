from tkinter import Label
import psycopg2 as pg
import random

#connection is established
con = pg.connect(host='localhost',
                 database='Railway',
                 user='postgres',
                 password='raj',
                 port=5432)

#curser is created
cur = con.cursor()


def payment_gateway(PNR):  # payment function to validate the payment
    mode = input("Enter the payment mode:")
    mode = mode.title()
    amount = random.choice(
        ['1020', '2011', '1560', '1542'])  # amount to be paid
    print("Amount to pay:", amount)
    # capatcha to type for processing the payment
    captcha_text = (random.choice(['127413', 'ABTYSA', '7861AB', 'yuja67']))
    print("Enter the Capatcha to make the payment\n", captcha_text)
    text = input()
    if(text == captcha_text):
        # generating random transaction id
        txn_id = str(round(random.random()*1000000))
        # query to execute after reservation is made as PNR is a foreign key
        querry = "insert into payment_gateway values("+txn_id + \
            ","+"'"+mode+"'"+","+amount+","+PNR+")"
        return querry  # returning the string to execute
    else:
        return 0  # In case of wrong capatcha


def View_Reservation(PNR):  # defination to view the status of the reservation
    string = "Select * from passengers where PNR = "+PNR
    # select query to get the details of the passengers from PNR
    cur.execute(string)
    out = cur.fetchall()
    l = ["PNR", "NAME", "JOURNEY DATE", "TRAIN NUMBER", "STATUS"]
    for i in range(len(l)):
        print(l[i], " :", out[0][i], end="\t")


# defination to cancel the perticular reservation from passengers entity
def Cancel_Reservation(PNR):
    print("Present status\n")
    View_Reservation(PNR)
    string = "Update passengers set reservation_status = 'Cancelled' where PNR ="+PNR
    cur.execute(string)  # update query to cancel the ticket
    print("\nNew Status\n")
    View_Reservation(PNR)
    con.commit()


def New_Reservation():
    Name = input("Enter you're name: ")
    Train_Number = input("Enter the Train number: ")
    DOJ = input("Enter the Date of Journey (DD-MMM-YYYY): ")
    PNR = str(round(random.random()*10000))
    Status = random.choice(['Confirmed', 'RAC', 'Waiting'])
    txn_query = payment_gateway(PNR)
    query = "insert into passengers values("+PNR+','+"'"+Name + \
        "'"+','+"'"+DOJ+"'"+','+Train_Number+','+"'"+Status+"'"+")"
    if(txn_query == 0):
        print("Payment failes due to wrong Capatcha")
        return

    cur.execute(query)  # query to insert into passengers entity
    cur.execute(txn_query)  # query to insert into payment_gateway entity
    View_Reservation(PNR)
    con.commit()

def Available_Trains():
    query="select * from train"
    cur.execute(query)
    out=cur.fetchall()
    for i in out:
        print(i)


print("Welcome to the DataBase Managemet System")
print("Enter the operation you want to do", end="\n")
print("1.Related to Reservation\n2.Availability of Trains\n")
ch = int(input())

if(ch == 1):
    print("1.View the Reservation Status\n2.Make a new Reservation\n3.Cancel the Reservation")
    Rch = int(input())
    if(Rch == 1):
        PNR = input("Enter the PNR \n")
        View_Reservation(PNR)
    elif Rch == 2:
        New_Reservation()
    elif(Rch == 3):
        PNR = input("Enter the PNR \n")
        Cancel_Reservation(PNR)

if(ch == 2):
    print("1.View Available Trains")
    Available_Trains()
cur.close()
con.close()
