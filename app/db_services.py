from flask_mysqldb import MySQL

conn = MySQL()

workers_field_titles_full = ["name","last_name","age","sex","birth_date","curp", "elector_key", "ife", "entry_date",
                        "position","branch","minutely_salary","hourly_salary","daily_salary",
                        "biweekly_salary","monthly_salary","vacation_assigned_days","vacation_taken_days",
                        "vacation_remaining_days"]
workers_field_titles_less = ["id","name","position","daily_salary","biweekly_salary","monthly_salary"]

def get_user(usr_name: str) -> dict:
    crs = conn.connection.cursor()
    crs.execute(f"SELECT name,password FROM TB_Auth_Users WHERE name='{usr_name}'")
    result = crs.fetchone()
    if result:
        return {"usr-name": result[0], "usr-passwrd":result[1]}
    return {} 
def get_workers_resumed_data()->dict:
    crs = conn.connection.cursor()
    crs.execute(""" SELECT id,name, position, daily_salary, biweekly_salary, monthly_salary
                FROM TB_Employees""")
    query_result = crs.fetchall()
    return_dict = {}
    row_count = 1
    for row in query_result:
        tmp_dict = {}
        for key,value in zip(workers_field_titles_less, row):
            tmp_dict[key] = value
        return_dict[f"worker_{row_count}"] = tmp_dict
        row_count+=1
    return return_dict

def get_single_worker_data(id)->dict:
    crs = conn.connection.cursor()
    crs.execute(f"""SELECT name,last_name,age,sex,birth_date,curp, elector_key, ife, entry_date,
                        position,branch,minutely_salary,hourly_salary,daily_salary,
                        biweekly_salary,monthly_salary,vacation_assigned_days,vacation_taken_days,
                        vacation_remaining_days 
                FROM TB_Employees
                WHERE id={id}""")
    query_result = crs.fetchall()
    return_dict = {}
    for row in query_result:
        for key, value in zip(workers_field_titles_full, row):
            return_dict[key] = str(value)
    return return_dict

def get_workers_full_data()->dict:
    crs = conn.connection.cursor()
    crs.execute("""SELECT name,last_name,age,sex,birth_date,curp,entry_date,
                        position,branch,minutely_salary,hourly_salary,daily_salary,
                        biweekly_salary,monthly_salary,vacation_assigned_days,vacation_taken_days,
                        vacation_remaining_days 
                FROM TB_Employees""")
    result = crs.fetchall()
    return_dict = {}
    row_count = 1
    for row in result:
        tmp_dict = {}
        for key, value in zip(workers_field_titles_full, row):
            tmp_dict[key] = str(value)
        return_dict[f"worker_{row_count}"] = tmp_dict
        row_count+=1
    return return_dict
