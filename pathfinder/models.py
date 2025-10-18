import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_user(first, last, email, password_hash, education=None, cgpa=None):
    db = get_db_connection()
    cur = db.cursor()
    sql = "INSERT INTO Users (first_name, last_name, email, password_hash, highest_education, cgpa) VALUES (%s,%s,%s,%s,%s,%s)"
    cur.execute(sql,(first,last,email,password_hash,education,cgpa))
    db.commit()
    uid = cur.lastrowid
    cur.close(); db.close()
    return uid

def find_user_by_email(email):
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close(); db.close()
    return user

def get_all_careers():
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Careers")
    rows = cur.fetchall()
    cur.close(); db.close()
    return rows

def get_career_by_id(career_id):
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Careers WHERE career_id=%s", (career_id,))
    row = cur.fetchone()
    cur.close(); db.close()
    return row

# Add more helpers for skills, user skills, interests as needed
