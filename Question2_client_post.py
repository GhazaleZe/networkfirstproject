import requests
import os
import time
import platform
import sys

flag = 1
loop_user = 1
loop_admin = 1
PARAMS = CMD = USERNAME = PASSWORD = ROLE = PARAMS1 = TOKEN = RESPONSE = TICK_ID = ""
first_name = last_name = ""
HOST = "127.0.0.1"
PORT = "8778"
SUBJECT = BODY = STATUS = ""


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def users_func():
    print("What you can do as a USER ,Please enter a number :\n"
          "1.send a ticket\n"
          "2.get a ticket\n"
          "3.close a ticket\n"
          "4.logout")


# ______________________________________________________________________
def admin_func():
    print ("What you can do as an admin , Please enter a number:\n"
           "1.send a ticket\n"
           "2.get a ticket\n"
           "3.reply a ticket\n"
           "4.change status\n"
           "5.logout")


# _______________________________________________________________________
# def sendticket():

# _____________________________________________________________
def __postcr__():
    return "http://" + HOST + ":" + PORT + "/" + CMD + "?"


# ___________________________________________________________
while True:
    clear()
    print ("""Welcome to TICKET client
     Please choose what you want to do
     1.signup
     2.login
     3.exit""")
    chosen = sys.stdin.readline()
    if chosen[:-1] == '1':
        print("To Create New Account Enter The Authentication")
        print("FIRST NAME :")
        first_name = sys.stdin.readline()[:-1]
        print ("LAST NAME :")
        last_name = sys.stdin.readline()[:-1]
        print("USERNAME : ")
        USERNAME = sys.stdin.readline()[:-1]
        print("PASSWORD : ")
        PASSWORD = sys.stdin.readline()[:-1]
        print("your role:User or  Admin")
        ROLE = sys.stdin.readline()[:-1]
        CMD = "signup"
        clear()
        PARAMS = {'username': USERNAME, 'password': PASSWORD, 'role': ROLE}
        r = requests.post(__postcr__(), PARAMS).json()
        if str(r['message']) == "Signed Up Successfully":
            print("Your Account Is Created\n" + "Your Username :" + USERNAME + "\nYour Role :" + ROLE)
            flag = 2
            break
        else:
            print(r['message'] + "\n" + "Try Again")
            input("Press Any Key To Continue ...")
            clear()
    # _________login________________________________________________________________________________
    if chosen[:-1] == '2' or flag == 2:
        clear()
        flag = 1
        print("USERNAME : ")
        USERNAME = sys.stdin.readline()[:-1]
        print("PASSWORD : ")
        PASSWORD = sys.stdin.readline()[:-1]
        print("your role:User or  Admin")
        ROLE = sys.stdin.readline()[:-1]
        CMD = "login"
        clear()
        PARAMS = {'username': USERNAME, 'password': PASSWORD, 'role': ROLE}
        r = requests.post(__postcr__(), PARAMS).json()
        if str(r['message']) == "Logged in Successfully":
            print("Your have logged in\n" + "Your Username :" + USERNAME + "\nYour Role :" + ROLE)
            if ROLE == "User" and loop_user == 1:
                while loop_user == 1:
                    clear()
                    users_func()
                    user_select = sys.stdin.readline()[:-1]
                    # send ticket*****************************
                    if user_select == '1':
                        print ("Type a subject:")
                        SUBJECT = sys.stdin.readline()[:-1]
                        print ("Type body of your ticket :")
                        BODY = sys.stdin.readline()[:-1]
                        TOKEN = r['token']
                        CMD = "sendticket"
                        PARAMS = {'body': BODY, 'subject': SUBJECT, 'token': TOKEN}
                        r1 = requests.post(__postcr__(), PARAMS).json()
                        if str(r1['message']) == "Ticket Sent Successfully":
                            print ("Ticket sent Successfully\n")
                            # input("Press Any Key To Continue ...")

                        else:
                            print(r1['message'] + "\n" + "Try Again")
                            # input("Press Any Key To Continue ...")
                            clear()
                    # **get a ticket****************************************
                    elif user_select == '2':
                        TOKEN = r['token']
                        PARAMS = {'token': TOKEN}
                        CMD = "getticketcli"
                        r1 = requests.post(__postcr__(), PARAMS).json()
                        if str(r1['code']) == "200":
                            print ("here must be tickets of this user\n")
                        # break
                    # ****close ticket**********************************
                    elif user_select == '3':
                        CMD = "closeticket"
                        TOKEN = r['token']
                        print ("enter a id of the ticket you want to close: ")
                        TICK_ID = sys.stdin.readline()
                        PARAMS = {'token': TOKEN, 'ticket_id': TICK_ID}
                        r1 = requests.post(__postcr__(), PARAMS).json()
                        if str(r1['message']) == "Ticket closed Successfully":
                            print ("ticket with id =" + TICK_ID + "is closed")
                        # break
                    # *log out*******************************************
                    elif user_select == '4':
                        CMD = "logout"
                        clear()
                        PARAMS = {'username': USERNAME, 'password': PASSWORD, 'role': ROLE}
                        r1 = requests.post(__postcr__(), PARAMS).json()
                        if str(r1['message']) == "Logged out Successfully":
                            print("Logged out Successfully")
                            loop_user = 2
                    else:
                        print ("enter a number between 1 to 4")
                        clear()
                # input("Press Any Key To Continue ...")
                # break
            elif ROLE == "Admin" and loop_admin == 1:
                while loop_admin == 1:
                    admin_func()
                    admin_select = sys.stdin.readline()[:-1]
                    # send ticket*****************************
                    if admin_select == '1':
                        print ("Type a subject:")
                        SUBJECT = sys.stdin.readline()[-1]
                        print ("Type body of your ticket :")
                        BODY = sys.stdin.readline()[-1]
                        TOKEN = r['token']
                        CMD = "sendticket"
                        PARAMS = {'body': BODY, 'subject': SUBJECT, 'token': TOKEN}
                        r1 = requests.post(__postcr__(), PARAMS).json()
                        if str(r1['message']) == "Ticket Sent Successfully":
                            print ("Ticket sent Successfully\n")
                            # input("Press Any Key To Continue ...")
                        else:
                            print(r1['message'] + "\n" + "Try Again")
                            # input("Press Any Key To Continue ...")
                            clear()
                    # **get ticket mod**************************
                    elif admin_select == "2":
                        print ("sorry this function can't work now")
                    elif admin_select == "3":
                        CMD = "restoticketmod"
                        print ("please type your response")
                        RESPONSE = sys.stdin.readline()[:-1]
                        TOKEN = r['token']
                        print ("please enter the id of ticket you want to response :")
                        TICK_ID = sys.stdin.readline()[:-1]
                        PARAMS1 = {'response': RESPONSE, 'token': TOKEN, 'ticket_id': TICK_ID}
                        r1 = requests.post(__postcr__(), PARAMS1).json()
                        if str(r1['message']) == "Response to Ticket Sent Successfully":
                            print ("Response to Ticket with id : '" + TICK_ID + "' have Sent Successfully")
                    elif admin_select == "4":
                        CMD = "changestatus"
                        TOKEN = r['token']
                        print ("enter the id of  ticket you want to change: ")
                        TICK_ID = sys.stdin.readline()
                        print (" enter a status : Open , Suspend ,Close")
                        STATUS = sys.stdin.readline()[:-1]
                        PARAMS1 = {'token': TOKEN, 'ticket_id': TICK_ID ,'status' : STATUS}
                        r1 = requests.post(__postcr__(), PARAMS1).json()
                        if str(r1['message']) == "Status Ticket Changed Successfully":
                            print ("ticket's status with id =" + TICK_ID + "has changed")
                        else:
                            print(r1['message'] + "\n" + "Try Again")
                    elif admin_select == "5":
                        CMD = "logout"
                        clear()
                        PARAMS = {'username': USERNAME, 'password': PASSWORD, 'role': ROLE}
                        r1 = requests.post(__postcr__(), PARAMS).json()
                        if str(r1['message']) == "Logged out Successfully":
                            print("Logged out Successfully")
                            loop_admin = 2
                    else:
                        print ("please enter a number between 1 to 5")
        else:
            print(r['message'] + "\n" + "Try Again")
            # input("Press Any Key To Continue ...")
            clear()
            loop_admin =1
            loop_user =1
    # ____________________________________________________________________________________
    elif chosen[:-1] == '3':
        clear()
        sys.exit()
    else:
        print("Please enter a number between 1 and 3")
