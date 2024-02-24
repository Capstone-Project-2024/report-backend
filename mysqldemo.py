#Below is a demo of our app's API request saving functionality using MySQL.
#If you want to try it yourself you'll need to download MySQL Server and create a root user profile.
#Eventually, a version of this code will be integrated with our "app.py" file, but for now it just runs in the terminal on a local MySQL server.

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root", #Change this to whatever username you set up for your root user profile.
    passwd="notlostandfound5", #Change this to whatever password you set up for your root user profile.
)
mycursor = db.cursor(buffered=True)
mycursor.execute("CREATE DATABASE IF NOT EXISTS mysqldemo")

#Connector needs to be redeclared, now with the "database" field filled in since the database has been created. There's proabbly a better way to do this but it works for now.
db = mysql.connector.connect(
    host="localhost",
    user="root", #Again, replace this and the passwd field below to match your own profile info.
    passwd="notlostandfound5", #Replace this with the password you set up.
    database="mysqldemo"
)
mycursor = db.cursor(buffered=True)
mycursor.execute("CREATE TABLE IF NOT EXISTS Request (request_id int PRIMARY KEY AUTO_INCREMENT, subreddit VARCHAR(50), author VARCHAR(50))")

prompt_user = True
while prompt_user == True:
    print("Welcome to the Reddit Post API requester! What would you like to do?")
    print("1. Create a new request")
    print("2. Use a previous request")
    print("3. Delete a previous request")
    answer = input("Enter number of answer: ")

    if answer == "1":
        subreddit = input("\nEnter subreddit of desired post(s): ")
        author = input("\nEnter author of desired post(s): ")
        print("\nReturned API data would appear here.\n")
        while prompt_user == True:
            print("Would you like to save this request for later use?")
            save_request = input("Enter y/n: ")
            if save_request == "y":
                mycursor.execute("INSERT INTO Request (subreddit, author) VALUES (%s,%s)", (subreddit, author))
                db.commit()
                print("\nRequest has been saved.\n")
                break
            elif save_request == "n":
                print("\n")
                break
            else:
                print("\nInvalid input. Please try again.\n")

    elif answer == "2":
        print("\nPrevious requests:")
        mycursor.execute("SELECT * FROM Request")
        for request in mycursor:
            print(request)
        request_id_string = input("\nEnter request_id of the request you want to use: ")
        request_id = int(request_id_string)
        mycursor.execute("SELECT * FROM Request WHERE request_id = '%s'" %request_id)
        print("\nReturned API data would appear here.\n")

    elif answer == "3":
        print("\nPrevious requests:")
        mycursor.execute("SELECT * FROM Request")
        for request in mycursor:
            print(request)
        request_id_string = input("\nEnter request_id of the request you want to delete: ")
        request_id = int(request_id_string)
        mycursor.execute("DELETE FROM Request WHERE request_id = '%s'" %request_id)
        db.commit()
        print("\nRequest %s has been successfully deleted.\n" %request_id)

    else:
        print("\nInvalid input. Please try again.\n")
