from flask_mysqldb import MySQL, cursors

conn = MySQL()

def get_user(usr_name: str) -> dict:
    crs = conn.connection.cursor()
    crs.execute(f"SELECT name,password FROM TB_Auth_Users WHERE name='{usr_name}'")
    return dict(crs.fetchall())
