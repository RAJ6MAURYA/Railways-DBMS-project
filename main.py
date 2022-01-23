
import psycopg2 as pg
import tkinter as tk
import PyPDF2
from  PIL import Image, ImageTk
import random

#connection is established
con = pg.connect(host='localhost',
                 database='Railway',
                 user='postgres',
                 password='raj',
                 port=5432)

#curser is created
cur = con.cursor()


def PNR_validation(PNR):
    query = "Select * from passengers where PNR = "+PNR
    cur.execute(query)
    out = cur.fetchall()
    if not out:
        print("\n###################        NO RECORD IS FOUND | ENTER A VALID PNR       ##################################\n".center(80))
        return False
    else:
        return True


def payment_gateway(PNR):  # payment function to validate the payment
    Payment_Mode = input("\nEnter the payment Payment_Mode:\n").title()
    amount = random.choice(
        ['1020', '2011', '1560', '1542'])  # amount to be paid
    print("\nAmount to pay:", amount)
    # captcha to type for processing the payment
    captcha_text = (random.choice(['127413', 'ABTYSA', '7861AB', 'yuja67']))
    print("\nEnter the Captcha to make the payment\n", captcha_text)
    text = input()
    if(text == captcha_text):
        # generating random transaction id
        txn_id = str(round(random.random()*1000000))
        # query to execute after reservation is made as PNR is a foreign key
        query = "insert into payment_gateway values("+txn_id + \
            ","+"'"+Payment_Mode+"'"+","+amount+","+PNR+")"
        return query  # returning the string to execute
    else:
        return 0  # In case of wrong Captcha


def View_Reservation(PNR):  # def to view the status of the reservation
    query = "Select * from passengers where PNR = "+PNR
    # select query to get the details of the passengers from PNR
    cur.execute(query)
    out = cur.fetchall()
    if(PNR_validation(PNR) == False):
        return
    Heading = ["PNR", "NAME", "DATE", "TRAIN NO", "STATUS"]
    print(end="\n")
    for i in Heading:
        print("%-20s" % i, end="")
    print(end="\n")
    for i in range(len(out)):
        for j in range(len(out[i])):
            print("%-20s" % out[i][j], end="")
    print(end="\n")


# definition to cancel the perticular reservation from passengers entity
def Cancel_Reservation(PNR):
    print("\nPresent status\n")
    if View_Reservation(PNR) == False:
        return
    string = "Update passengers set reservation_status = 'Cancelled' where PNR ="+PNR
    cur.execute(string)  # update query to cancel the ticket
    print("\nNew Status\n")
    View_Reservation(PNR)
    con.commit()


def New_Reservation():
    Name = input("\nEnter your name: ")
    Available_Trains()
    Train_Number = input("\nEnter the Train number: ")
    DOJ = input("\nEnter the Date of Journey (DD-MMM-YYYY): ")
    PNR = str(round(random.random()*10000))
    Status = random.choice(['Confirmed', 'RAC', 'Waiting'])
    txn_query = payment_gateway(PNR)
    query = "insert into passengers values("+PNR+','+"'"+Name + \
        "'"+','+"'"+DOJ+"'"+','+Train_Number+','+"'"+Status+"'"+")"
    if(txn_query == 0):
        print("\n*************************        PAYMENT FAILED DUE TO WRONG CAPTCHA      **************************\n".center(80))
        return

    cur.execute(query)  # query to insert into passengers entity
    cur.execute(txn_query)  # query to insert into payment_gateway entity
    View_Reservation(PNR)
    con.commit()


def Available_Trains():
    query = "select * from train"
    cur.execute(query)
    out = cur.fetchall()
    print("\nTrain no\tTrain Name\t\tSeats Available\n")
    for i in out:
        print(i[0], "\t\t", i[1], "\t\t", i[4])


def user():
    while(True):
        print("\n1.Related to Reservation\t2.Availability of Trains\t3.EXIT")
        ch = int(input("Enter: "))
        if(ch == 1):
            print(
                "\n1.View the Reservation Status\t2.Make a new Reservation\t3.Cancel the Reservation")
            Rch = int(input("Enter:"))
            if(Rch == 1):
                PNR = input("\nEnter the PNR \n")
                View_Reservation(PNR)
            elif Rch == 2:
                New_Reservation()
            elif(Rch == 3):
                PNR = input("\nEnter the PNR \n")
                Cancel_Reservation(PNR)
        if(ch == 2):
            print("\nAvailable Trains\n")
            Available_Trains()
        if(ch == 3):
            print("\nThank you, Have a good day".center(80))
            break


def admin():
    while(True):
        ch = int(input(
            "\n1.Passengers details\t2.Train details\t 3.Payment History\t4.Station details\t5.EXIT\nEnter: "))
        if(ch == 1):
            ich = int(
                input("1.View the details\t2.Update the details\t3.Delete the details\n"))
            cur.execute("select * from passengers")
            out = cur.fetchall()
            if not out:
                print(
                    "\n###################        NO RECORD IS FOUND     ##################################\n".center(80))
                continue
            else:
                Heading = ["PNR", "NAME", "DATE", "TRAIN NO", "STATUS"]
                print(end="\n")
                for i in Heading:
                    print("%-20s" % i, end="")
                print(end="\n\n")
                for i in range(len(out)):
                    for j in range(len(out[i])):
                        print("%-20s" % out[i][j], end="")
                    print(end="\n")
                print(end="\n")
            if(ich == 2):
                PNR = input("Enter the PNR: ")
                if PNR_validation(PNR) == False:
                    continue
                Name = input("\nEnter your name: ")
                Available_Trains()
                Train_Number = input("\nEnter the Train number: ")
                DOJ = input("\nEnter the Date of Journey (DD-MMM-YYYY): ")
                Status = random.choice(['Confirmed', 'RAC', 'Waiting'])
                query = "update passengers set P_name="+"'"+Name+"'"+",DOJ="+"'"+DOJ+"'" + \
                    ",Train_number="+Train_Number+",reservation_status="+"'"+Status+"'"+"where pnr="+PNR
                cur.execute(query)
                con.commit()
                View_Reservation(PNR)
            if(ich == 3):
                PNR = input("\nEnter the PNR: ")
                if PNR_validation(PNR) == False:
                    continue
                query = "Delete from passengers where pnr="+PNR
                View_Reservation(PNR)
                print("The Entry is deleted\n")
                cur.execute(query)
                con.commit()

        if(ch == 2):
            Available_Trains()
        if(ch == 3):
            cur.execute("select * from payment_gateway")
            out = cur.fetchall()
            head = ["Transaction ID", "Paymen Mode", "Amount", "PNR"]
            if not out:
                print(
                    "#############################        No Record Of Payment        #####################################")
                continue
            for i in head:
                print("%-20s" % i, end="")
            print(end="\n\n")
            for i in range(len(out)):
                for j in range(len(out[i])):
                    print("%-20s" % out[i][j], end="")
                print(end="\n")
        if(ch == 4):
            cur.execute("Select * from stations")
            out = cur.fetchall()
            head = ["Station Code", "Station Name"]
            for i in head:
                print("%-20s" % i, end="")
            print(end="\n\n")
            for i in range(len(out)):
                for j in range(len(out[i])):
                    print("%-20s" % out[i][j], end="")
                print(end="\n")
        if(ch == 5):
            print("Thank you. Have a nice day")
            break



# driver code
print("Welcome to the DataBase Managemet System".center(80))
ch = int(input("1.Admin\t2.User"))

if(ch == 1):
    password = input("Enter the password: ")
    if(password == "Raj123"):
        admin()
    else:
        print("###################################  Invalid Password        #########################################")
elif(ch == 2):
    user()
else:
    print("#######################################      Invalid Choice       ########################################")
cur.close()
con.close()
