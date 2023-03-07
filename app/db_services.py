import pymysql
from os import getenv

###
###     Methods starting with (get) will do SELECT operations
###     Methods starting with (set) will do INSERT operations
###

conn = pymysql.connect(
        host=getenv("MYSQL_HOST"),
        user=getenv("MYSQL_USER"),
        password=str(getenv("MYSQL_PASSWORD")),
        db=getenv("MYSQL_DB")
        ) 

column_headers_full = ["id","name","last_name","age","sex","birth_date","curp", 
                       "elector_key", "ine", "entry_date", "position","branch",
                       "minutely_salary","hourly_salary","daily_salary","biweekly_salary",
                       "monthly_salary","vacation_assigned_days","vacation_taken_days",
                       "vacation_remaining_days", "profile_pic"]
column_headers_less = ["id", "name", "last_name", "position", "daily_salary", "biweekly_salary",
                       "monthly_salary", "profile_pic"]
column_headers_short = ["id", "name", "last_name", "position", "branch", "profile_pic"]

def create_cursor():
    return conn.cursor()

def get_user(usr_name: str) -> dict:
    crs = create_cursor() 
    crs.execute(f"SELECT name,password FROM TB_Auth_Users WHERE name='{usr_name}'")
    result = crs.fetchone()
    if result:
        return {"usr-name": result[0], "usr-passwrd":result[1]}
    return {} 

def get_workers_resumed_data()->dict:
    crs = create_cursor() 
    crs.execute("""
        SELECT A.id, B.name, B.last_name, A.position, A.daily_salary, 
               A.biweekly_salary, A.monthly_salary, A.profile_pic
        FROM WRKR_Employee AS A INNER JOIN WRKR_Individual AS B
        ON A.id_individual = B.id
    """)
    query_result = crs.fetchall()
    return_dict = {}
    row_count = 1
    for row in query_result:
        tmp_dict = {}
        for key,value in zip(column_headers_less, row):
            tmp_dict[key] = value
        return_dict[f"worker_{row_count}"] = tmp_dict
        row_count+=1
    return return_dict

def get_workers_short_data()->dict:
    crs = create_cursor()
    crs.execute("""
        SELECT A.id, B.name, B.last_name, A.position, A.branch, A.profile_pic 
        FROM WRKR_Employee AS A INNER JOIN WRKR_Individual AS B
        ON A.id_individual=B.id
    """)
    query_result = crs.fetchall()
    return_dict = {}
    for row in query_result:
        tmp = {}
        worker_id = row[0]
        for key, value in zip(column_headers_short, row):
            tmp[key] = value
        return_dict["worker_"+str(worker_id)] = tmp
    return return_dict

def get_single_worker_data(id)->dict:
    crs = create_cursor() 
    crs.execute(f"""
        SELECT A.id, B.name, B.last_name, B.age, B.sex, B.birth_date,curp, B.elector_key, 
                B.ine, A.entry_date, A.position, A.branch, A.minutely_salary, A.hourly_salary,
                A.daily_salary, A.biweekly_salary, A.monthly_salary, A.vacation_assigned_days,
                A.vacation_taken_days, A.vacation_remaining_days, A.profile_pic
        FROM WRKR_Employee AS A INNER JOIN WRKR_Individual AS B
                ON A.id_individual=B.id
        WHERE A.id={id}
    """)
    query_result = crs.fetchall()
    return_dict = {}
    for row in query_result:
        for key, value in zip(column_headers_full, row):
            return_dict[key] = str(value)
    return return_dict

def get_workers_full_data()->dict:
    crs = create_cursor() 
    crs.execute("""
        SELECT A.id, B.name, B.last_name, B.age, B.sex, B.birth_date,curp, B.elector_key, 
                B.ine, A.entry_date, A.position, A.branch, A.minutely_salary, A.hourly_salary,
                A.daily_salary, A.biweekly_salary, A.monthly_salary, A.vacation_assigned_days,
                A.vacation_taken_days, A.vacation_remaining_days, A.profile_pic
        FROM WRKR_Employee AS A INNER JOIN WRKR_Individual AS B
                ON A.id_individual=B.id
    """)
    result = crs.fetchall()
    return_dict = {}
    row_count = 1
    for row in result:
        tmp_dict = {}
        for key, value in zip(column_headers_full, row):
            tmp_dict[key] = str(value)
        return_dict[f"worker_{row_count}"] = tmp_dict
        row_count+=1
    return return_dict

def set_worker_data(data:list)->bool:
    crs = create_cursor() 
    crs.execute("""INSERT INTO TB_Employees (
            name, last_name, age, sex, birth_date, curp, elector_key, ine, entry_date, 
            position,branch, minutely_salary, hourly_salary, daily_salary, 
            biweekly_salary, monthly_salary,vacation_assigned_days,  profile_pic 
        )
        VALUES (
            '{}', '{}', '{}',  '{}', '{}', '{}', '{}', '{}', '{}', '{}', 
            '{}','{}', '{}', '{}', '{}', '{}', '{}', '{}'
        ) """.format(*data))
    conn.connection.commit()
    result = crs.rowcount
    return result > 0

def del_worker_data(id)->bool:
    crs = create_cursor()
    crs.execute(f"DELETE FROM TB_Employees WHERE id={id}")

    conn.connection.commit()
    result = crs.rowcount
    return result > 0
