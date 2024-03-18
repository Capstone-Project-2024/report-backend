#See datadive.sql before running the following
#This is essentially the code we need for registering/logging in users. All it needs is a UI.

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="notlostandfound5",
    database="datadive"
)
mycursor = db.cursor(buffered=True)

prompt_user = True
while prompt_user == True:
    print("What would you like to do?")
    print("1. Login")
    print("2. Register")
    answer = input("Enter number of answer: ")

    if answer == "1":
        while prompt_user == True:
            name = input("\nEnter username: ")
            mycursor.execute("SELECT user_name FROM users")
            user_names_list = []
            for user_name in mycursor:
                user_names_list.append(user_name[0])
            exists = name in user_names_list
            if exists == True:
                password = input("\nEnter password: ")
                mycursor.execute("SELECT user_password FROM users WHERE user_name = '%s'" %name)
                user_passwords_list = []
                for user_password in mycursor:
                    user_passwords_list.append(user_password[0])
                compared_password = user_passwords_list[0]
                if password == compared_password:
                    print("\nSuccessfully logged in\n")
                    break
                else:
                    print("\nIncorrect password. Login failed.\n")
                    break
            elif exists == False:
                print("\nUser with that name does not exist. Please try again. ")
                continue
    
    elif answer == "2":
        user_name = input("\nEnter username: ")
        user_password = input("\nEnter password: ")
        mycursor.execute("INSERT INTO users (user_name, user_password) VALUES (%s,%s)", (user_name, user_password))
        db.commit()
        print("\nAccount successfully created.\n")

    else:
        print("\nInvalid input. Please try again.\n")