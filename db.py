import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()  

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
# print(host, user, password, database)
def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except mysql.connector.Error as err:
        print("An error occurred:", err)
        exit(1)
    return mydb

