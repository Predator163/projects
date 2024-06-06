from prettytable import PrettyTable as p
import mysql.connector as m

c = m.connect(host = 'localhost',user = 'root',passwd =  'student')
r = c.cursor(buffered = True)

r.execute("create database if not exists train_management")

query = "use train_management"
r.execute(query)

def new_train():
    try:
        name = input("Enter the new name of the train: ")
        no = int(input("Enter the new no of the train: "))
        starting = input("Enter the starting point of the train: ")
        destination = input("Enter the destination of the train: ")
        seats = int(input("Number of seats available in the train: "))
        extra_specifications = input("Enter if any specifications(optional): ")

        query = "insert into train_details values('{}',{},'{}','{}','{}',{})".format(name,no,starting,destination,extra_specifications,seats)
        r.execute(query)
        c.commit()

        a = p(["NAME OF THE TRAIN","TRAIN NO","STARTING POINT","DESTINATION","SEATS AVAILABLE","EXTRA SPECIFICATIONS(IF MENTIONED)"])
        a.add_row([name,no,starting,destination,seats,extra_specifications])
        print(a)

        take = input("IF YOU WANT TO UPDATE PRESS Y OR ANY OTHER KEY TO CONTINUE: ")
        if take.lower() == 'y':
            update()
        else:
            take = input("Enter your choice for entering a new train Y(Yes) or N(No) for main menu: ")
            while take.lower() == 'y':
                new_train()
            else :
                mainmenu()
    except m.Error as err:
        print(err)
        if err == "1062 (23000): Duplicate entry '{}' for key 'PRIMARY'".format(no):
            print("TRAIN NO IS ALREADY PRESENT")

def reservation():
    try:
        trains()
        show_trains()

        name = input("Enter your name: ")
        train = int(input("Enter the train number for your journey: "))
        berth = input("Choice of berth: ")
        meals = input("Meals Requirement(Yes/NO): ")
        departure = input("Date of departure(YYYY-MM-DD): ")

        query = "select * from train_details where train_no = '{}'".format(train)
        r.execute(query)
        data = r.fetchone()
        b = data[0]

        query = "create table if not exists reservation(NAME varchar(30) not null,TRAIN varchar(40) not null,CHOICE_OF_BERTH varchar(10),MEALS varchar(3) not null,DATE_OF_DEPARTURE date not null)"
        r.execute(query)

        query = "insert into reservation values('{}','{}','{}','{}','{}')".format(name,b,berth,meals,departure)
        r.execute(query)
        c.commit()

        a = p(["NAME","TRAIN_NAME","BERTH","MEALS(REQUIRED)","DEPARTURE"])
        a.add_row([name,b,berth,meals,departure])
        print(a)
        print("YOUR RESERVATION IS COMPLETED SUCCESSFULLY | HAVE A SAFE JOURNEY")

        query = "select seats_available from train_details where train_no = '{}'".format(train)
        r.execute(query)
        data = r.fetchall()

        seats = int(data[0][0])
        seats -=1
        if seats == 0:
            print("SEATS ARE FILLED COMPLETELY IN THE TRAIN")
        else:
            query = "update train_details set seats_available = '{}' where train_no = {}".format(seats,train)
            r.execute(query)
            c.commit()

            choice = input("PRESS Y FOR DOING ONE MORE RESERVATION AND ANY OTHER KEY TO EXIT TO MAIN MENU: ")

            if choice.lower() == 'y':
                reservation()
            else:
                mainmenu()

    except m.Error:
        a = input("THERE ARE NO TRAINS AVAILABLE PLEASE ADD A NEW TRAIN PRESS Y OR ANY OTHER KEY TO RETURN TO MAIN MENU:")
        if a.lower() == 'y':
            new_train()
        else:
            mainmenu()

def show_trains():
    try:
        starting = input("Enter the starting point of your journey: ")
        destination = input("Enter the destination of your journey: ")

        query = "select * from train_details where STARTING_POINT = '{}' AND DESTINATION = '{}'".format(starting,destination)
        r.execute(query)
        data = r.fetchall()

        a = p(["TRAIN_NAME","TRAIN_NUMBER","STARTING_POINT","DESTINATION","EXTRA_SPECIFICATIONS","SEATS AVAILABLE"])
        if data == []:
            print('THERE ARE NO TRAINS AVAILABLE BETWEEN THE ENTERED STATIONS.')
            choice = input("Enter Y for doing reservation again or any other key to return to main menu: ")
            if choice.lower() == 'y':
                reservation()
            else:
                mainmenu()
        else:
            print("\t\t\t\tAVAILABLE TRAINS")
            for i in data:
                a.add_row(i)
            print(a)   

    except :
        print("ERROR")
        print("FIRST CHECK THE DETAILS OF TRAINS FOR YOUR INFO GO PRESS '1' IN MAINMENU")
        mainmenu()

def login_id():
    try:
        a = input("Enter if registered(Y) or not(N): ")
        if a.lower() == 'y':
            login()     
        elif a.lower() == 'n':
            name = input("Enter your name: ")
            phone = int(input("Enter phone number: "))
            if len(str(phone)) != 10:
                print("Enter 10 digits!")
                login_id()
            else:
                age = int(input("Enter the age: "))
                if age < 18:
                    print("YOU MUST BE 18 YEARS OLD FOR DOING THIS ACTIVITY")
                    exit()
                
                else:
                    aadhaar = int(input("Enter your aadhaar number: "))
                    if len(str(aadhaar)) != 12:
                        print("Enter 12 digits!")
                        login_id()
                    else:
                        address = input("Enter the Village/Town/City: ")
                        pincode = int(input("Enter the Pin Code: "))

                        query = "create table if not exists USERID(NAME varchar(30) not null,CONTACT_NO bigint(10) not null,AADHAAR_NO bigint(13) primary key,ADDRESS varchar(30) not null,PINCODE int(6) not null)"
                        r.execute(query)

                        query = "insert into userid values('{}',{},{},'{}',{})".format(name,phone,aadhaar,address,pincode)
                        r.execute(query)
                        c.commit()

                        a = p(["NAME","PHONE NUMBER","AADHAAR NUMBER","ADDRESS","PINCODE"])
                        a.add_row([name,phone,aadhaar,address,pincode])
                        print(a)

                        
                        user_id = input("CREATE A NEW USER ID(USE ONLY CAPITAL LETTERS): ")
                        username = input("ENTER YOUR NEW USERNAME: ")
                        password = input("ENTER YOUR NEW PASSWORD: ")

                        query = "create table if not exists LOGIN_ID(USER_ID varchar(30) primary key,USERNAME varchar(30) not null,password varchar(30) not null)"
                        r.execute(query)

                        query = "insert into login_id values('{}','{}','{}')".format(user_id,username,password)
                        r.execute(query)
                        c.commit()

                        a = p(["USER ID","USERNAME","PASSWORD"])
                        a.add_row([user_id,username,password])
                        print(a) 
                        
                        update = input("DO YOU WANT TO UPDATE THE DETAILS OF LOGIN PRESS Y OR ANY OTHER KEY: ")
                        if update.lower() == 'y':
                            edit()
                            login()
                        else:
                            login()

        else:
            print("INVALID INPUT")
            login_id()

    except m.Error as err:
        print(err)
    login_id()

def personal_info():
    try:
        user = input("Enter Name: ")
        query = "select * from userid where name = '{}'".format(user)
        r.execute(query)
        data = r.fetchall()
        if data == []:
            print("THERE ARE NO USERS WITH THE GIVEN NAME")
        else:
            a = p(["NAME","PHONE","AADHAAR","ADDRESS","PINCODE"])
            a.add_row([data[0][0],data[0][1],data[0][2],data[0][3],data[0][4]])
            print(a)
    except m.Error as err:
        print(err)

def login():
    try:
        print("\t\t\t\t"+"#"*40)
        print("\t\t\t\t"+'\tLOGIN WITH YOUR CREDENTIALS')
        print("\t\t\t\t"+'#'*40)

        username = input("Enter your username: ").strip()
        query = "select username from login_id where username = '{}'".format(username)
        r.execute(query)
        data = r.fetchone()

        if data != None: 
            if data[0].strip() == username:
                password = input("Enter your password: ")

                query = "select password from login_id where username = '{}'".format(username)
                r.execute(query)
                b = r.fetchone()

                if b == None:
                    print("PLEASE TRY AGAIN")
                    login()

                elif b[0].lower() != password.lower():
                    print("!INVALID PASSWORD TRY AGAIN")
                    choice  = input("IF YOU HAVEN'T REGISTERED YET PRESS Y or ANY OTHER KEY FOR TRY AGAIN:")
                    if choice.lower() == 'y':
                        login_id()
                        login()
                    else:
                        login()

                else:
                    print("\t\t\t"+"*"*56)
                    print("\t\t\t WELCOME TO CHITTOOR DISTRICT RAILWAY MANAGEMENT SYSTEM ")
                    print("\t\t\t"+"             PLEASE USE CAPITAL LETTERS ONLY            ")
                    print("\t\t\t"+"*"*56)
                    mainmenu()

            else:
                print("BEWARE OF CAPSLOCK(USE ONLY CAPITAL LETTERS)")
                print("USERNAME NOT FOUND")
                print("TRY AGAIN")
                login() 

        else:
            print("BEWARE OF CAPSLOCK(USE ONLY CAPITAL LETTERS)")
            print("USERNAME NOT FOUND")
            print("TRY AGAIN")
            login()  
    except m.Error as err:
        print(err)

def trains():
        
        query = "create table if not exists train_details(TRAIN_NAME varchar(30) not null,TRAIN_NO int(5) primary key,STARTING_POINT varchar(30),DESTINATION varchar(30),EXTRA_SPECIFICATIONS varchar(30),SEATS_AVAILABLE int(3) not null)"
        r.execute(query)

        query = "insert into train_details values('KERALA EXPRESS',12625,'KALIKIRI','CHITTOOR','NONE',90)"
        check(12625, query)

        query = "insert into train_details values('SWARNA JAYANTI',12644,'TIRUPATI','CHITTOOR','NONE',90)"
        check(12644, query)

        query = "insert into train_details values('ERS MILLENUM EX',12646,'KALIKIRI','MADANAPALLE','NONE',90)"
        check(12646, query)

        query = "insert into train_details values('GURUDEV EXPRESS',12659,'PUNGANUR','CHITTOOR','NONE',90)"
        check(12659, query)

        query = "insert into train_details values('BHUBANESHWAR EXP',12846,'MADANAPALLE','PUNGANUR','NONE',90)"
        check(12846, query)
        

        query = "select * from train_details"
        r.execute(query)
        data = r.fetchall()

        a = p(["NAME","TRAIN NO","STARTING","DESTINATION",'EXTRA SPECIFICATIONS',"SEATS AVAILABLE"])
        for i in data:
            a.add_row(i)

        print(a)

def check(train_no, query):
    query1 = "select * from train_details where train_no = {}".format(train_no)
    r.execute(query1)
    data = r.fetchall()
    if data ==[]:
        
        r.execute(query)
    
        c.commit()

def edit():
    userid = input("Enter your userid you want to update: ")

    query = "select * from login_id where user_id = '{}'".format(userid)
    r.execute(query)
    data = r.fetchall()

    if data == []:
        print("ENTER A VALID USERID!")
        edit()
    else:
        a = p(["USERNAME","PASSWORD"])
        a.add_row([data[0][1],data[0][2]])
        print(a)

        print("1.UPDATE USERNAME")
        print("2.UPDATE PASSWORD")
        choice = int(input("ENTER YOUR CHOICE: "))

        if choice == 1:
            new_user = input("ENTER NEW USERNAME: ")

            query = "update login_id set username = '{}' where user_id = '{}'".format(new_user,userid)
            r.execute(query)
            c.commit()

            query = "select * from login_id where user_id = '{}'".format(userid)
            r.execute(query)
            data = r.fetchone()
            
            a = p(["NEW USERNAME"])
            a.add_row([data[1]])
            print(a)
            login()
        
        elif choice == 2:
            new_pwd = input("ENTER NEW PASSWORD: ")

            query = "update login_id set password = '{}' where user_id = '{}'".format(new_pwd,userid)
            r.execute(query)
            c.commit()

            query = "select * from login_id where user_id = '{}'".format(userid)
            r.execute(query)
            data = r.fetchone()
            
            a = p(["NEW PASSWORD"])
            a.add_row([data[2]])
            print(a)
            login()
        
        else:
            print("INVALID INPUT!")
            edit()
def update():
    try:
        take =  int(input("ENTER THE TRAIN_NO YOU WANT TO UPDATE: "))
        print("1.TRAIN NAME")
        print("2.STARTING POINT")
        print("3.DESTINATION")
        print("4.SEATS")

        query = "select * from train_details where train_no = {}".format(take)
        r.execute(query)
        data = r.fetchone()

        a = p(["TRAIN NAME","TRAIN NO","STARTING POINT","DESTINATION","EXTRA SPECIFICATIONS","SEATS AVAILABLE"])
        a.add_row([data[0],data[1],data[2],data[3],data[4],data[5]])
        print(a)

        choice = int(input("ENTER THE NO YOU WANT TO UPDATE: "))
        if choice == 1:
            new_name = input("ENTER THE NEW NAME OF THE TRAIN: ")
            query = "update train_details set train_name = '{}' where train_no = {}".format(new_name,take)
            r.execute(query)
            c.commit()

            query = "select * from train_details where train_no = '{}'".format(take)
            r.execute(query)

            data = r.fetchone()
            print("\t\t\tUPDATED TRAIN DETAILS")
            a = p(["TRAIN NAME","TRAIN NO","STARTING POINT","DESTINATION","EXTRA SPECIFICATIONS","SEATS AVAILABLE"])
            a.add_row([data[0],data[1],data[2],data[3],data[4],data[5]])
            print(a)

        elif choice == 2:
            new_starting = input("ENTER THE NEW STARTING POINT OF THE TRAIN: ")
            query = "update train_details set starting_point = '{}' where train_no = {}".format(new_starting,take)
            r.execute(query)
            c.commit()

            query = "select * from train_details where train_no = {}".format(take)
            r.execute(query)

            data = r.fetchone()
            print("\t\t\tUPDATED TRAIN DETAILS")
            a = p(["TRAIN NAME","TRAIN NO","STARTING POINT","DESTINATION","EXTRA SPECIFICATIONS","SEATS AVAILABLE"])
            a.add_row([data[0],data[1],data[2],data[3],data[4],data[5]])
            print(a) 

        elif choice == 3:
            new_destination = input("ENTER THE NEW DESTINATION OF THE TRAIN: ")
            query = "update train_details set destination = '{}' where train_no = {}".format(new_destination,take)
            r.execute(query)
            c.commit()

            query = "select * from train_details where train_no = {}".format(take)
            r.execute(query)
            data = r.fetchone()

            print("\t\t\tUPDATED TRAIN DETAILS")
            a = p(["TRAIN NAME","TRAIN NO","STARTING POINT","DESTINATION","EXTRA SPECIFICATIONS","SEATS AVAILABLE"])
            a.add_row([data[0],data[1],data[2],data[3],data[4],data[5]])
            print(a)

        elif choice == 4:
            new_seats = int(input("UPDATE THE COUNT OF SEATS: "))
            query = "update train_details set seats_available = {} where train_no = {}".format(new_seats,take)
            r.execute(query)
            c.commit()
            query = "select * from train_details where train_no = {}".format(take)
            r.execute(query)
            data = r.fetchone()

            print("\t\t\tUPDATED TRAIN DETAILS")
            a = p(["TRAIN NAME","TRAIN NO","STARTING POINT","DESTINATION","EXTRA SPECIFICATIONS","SEATS AVAILABLE"])
            a.add_row([data[0],data[1],data[2],data[3],data[4],data[5]])
            print(a)
            
        else: 
            print("Invalid INPUT!!")
    except m.Error:
        print("ERROR")
        mainmenu()

def credits():
    print("\tTHIS PROJECT IS DONE BY")
    a = p(["NAME","CLASS","ROLL NO"])
    a.add_row(["M.SUMANTH KUMAR","XII","163"])
    a.add_row(["P.DILEEP KUMAR","XII","161"])
    a.add_row(["S.LOKESH KUMAR","XII","165"])
    print(a)

def show_ticket():
    try:
        name = input("Enter your name on the ticket: ")
        query = "select * from reservation where name ='{}'".format(name)
        r.execute(query)
        data = r.fetchall()
        if data == []:
            print("THERE ARE NO TICKETS WITH THE GIVEN NAME")
            ticket = input("Enter Y for finding a ticket or any other key to exit to main menu: ")
            if ticket.lower() == 'y':
                show_ticket()
            else:
                mainmenu()
        else:
            a = p(["NAME","TRAIN","CHOICE OF BERTH","MEALS","DATE OF DEPARTURE"])
            a.add_row(data[0])
            print(a)
    except m.Error:
        print("THERE ARE NO TICKETS WITH THE GIVEN NAME")

def delete():
    try:
        trains()

        d = int(input('Enter the train no which you want to delete:'))
        query = "select * from train_details where train_no = '{}'".format(d)
        r.execute(query)
        data = r.fetchone()
        if data != None:
            query = "delete from train_details where train_no = '{}'".format(d)
            r.execute(query)
            c.commit()
            print('The train has been deleted')
            print("\t\t\t!!DEFAULT TRAINS CANNOT BE DELETED!!")
        else:
            print('No train found with name {}'.format(d))

        trains()

    except m.Error:
        print(m.Error)
        mainmenu()
        

def mainmenu():
    print("1.DISPLAY TRAIN DETAILS")
    print("2.RESERVATION")
    print("3.PROFILE")
    print("4.CREDITS")
    print("5.EXIT")
    try:
        choice =  int(input("Enter your choice: "))
    except:
        print("INVALID INPUT")
        mainmenu()
    else:
        if choice == 1:
            print("1.DISPLAY THE TRAINS AVAILABLE")
            print("2.ADD A NEW TRAIN")
            print("3.UPDATE THE TRAIN DETAILS")
            print("4.DELETE INFO OF TRAIN")
            choice =  int(input("Enter your choice: "))
            if choice == 1:
                trains()
                again = input("DO YOU WANT TO CONTINUE press(Y) or ANY OTHER KEY TO EXIT: ")
                if again.lower() == 'y':
                    mainmenu()
                else:
                    print("THANK YOU AND VISIT AGAIN")
                    exit()

            elif choice == 2:
                new_train()
                again = input("DO YOU WANT TO CONTINUE press(Y) or ANY OTHER KEY TO EXIT: ")
                if again.lower() == 'y':
                    mainmenu()
                else:
                    print("THANK YOU AND VISIT AGAIN")
                    exit()

            elif choice == 3:
                update()
                again = input("DO YOU WANT TO CONTINUE press(Y) or ANY OTHER KEY TO EXIT: ")
                if again.lower() == 'y':
                    mainmenu()
                else:
                    print("THANK YOU AND VISIT AGAIN")
                    exit()
            
            elif choice == 4:
                delete()
                again = input("DO YOU WANT TO CONTINUE press(Y) or ANY OTHER KEY TO EXIT: ")
                if again.lower() == 'y':
                    mainmenu()
                else:
                    print("THANK YOU AND VISIT AGAIN")
                    exit()
            else:
                print("INVALID INPUT!")


        elif choice == 2:
            print("1.RESERVATION OF TRAIN")
            print("2.SHOW TICKET")
            choice =  int(input("Enter your choice: "))
            if choice == 1:
                reservation()
                again = input("DO YOU WANT TO CONTINUE press(Y) or ANY OTHER KEY TO EXIT: ")
                if again.lower() == 'y':
                    mainmenu()
                else:
                    print("THANK YOU AND VISIT AGAIN")
                    exit()
            elif choice == 2:
                show_ticket()
                again = input("DO YOU WANT TO CONTINUE press(Y) or ANY OTHER KEY TO EXIT: ")
                if again.lower() == 'y':
                    mainmenu()
                else:
                    print("THANK YOU AND VISIT AGAIN")
                    exit()
            else:
                print("INVALID INPUT!")

        elif choice == 3:
            print("1.ACCOUNT INFO")
            print("2.UPDATE PROFILE")
            choice =  int(input("Enter your choice: "))
            if choice == 1:
                personal_info()
                again = input("DO YOU WANT TO CONTINUE press(Y) or ANY OTHER KEY TO EXIT: ")
                if again.lower() == 'y':
                    mainmenu()
                else:
                    print("THANK YOU AND VISIT AGAIN")
                    exit()

            elif choice == 2:
                edit()
                again = input("DO YOU WANT TO CONTINUE press(Y) or ANY OTHER KEY TO EXIT: ")
                if again.lower() == 'y':
                    mainmenu()
                else:
                    print("THANK YOU AND VISIT AGAIN")
                    exit()
            
            else:
                print("INVALID INPUT!")
        
        elif choice == 4:
            credits()
            again = input("DO YOU WANT TO CONTINUE press(Y) or ANY OTHER KEY TO EXIT: ")
            if again.lower() == 'y':
                mainmenu()
            else:
                print("THANK YOU AND VISIT AGAIN")
                exit()
        
        elif choice == 5:
            print("THANK YOU AND VISIT AGAIN")
            exit()

        else:
            print("INVALID INPUT")
            again = input("DO YOU WANT TO CONTINUE press(Y) or ANY OTHER KEY TO EXIT: ")
            if again.lower() == 'y':
                mainmenu()
            else:
                print("THANK YOU AND VISIT AGAIN")
                quit()

login_id()
