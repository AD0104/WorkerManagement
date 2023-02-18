from flask_mysqldb import MySQL

conn = MySQL()

def get_user(usr_name: str) -> dict:
    crs = conn.connection.cursor()
    crs.execute(f"SELECT name,password FROM TB_Auth_Users WHERE name='{usr_name}'")
    result = crs.fetchone()
    if result:
        return {"usr-name": result[0], "usr-passwrd":result[1]}
    return {} 
