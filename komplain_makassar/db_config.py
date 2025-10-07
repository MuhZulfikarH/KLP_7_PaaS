import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="zul",        
        password="gowa2105",       
        database="komplain_db"
    )
