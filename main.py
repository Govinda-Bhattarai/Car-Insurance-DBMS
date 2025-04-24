import mysql.connector
import tabulate

connection: mysql.connector.CMySQLConnection
cursor: mysql.connector.connection_cext.CMySQLCursor


def insertToCar(data: dict):
    try:
        cursor.execute(
            f"INSERT INTO CAR VALUE ('{data['engine_no']}', {data['owner_id']}, '{data['make']}', '{data['model']}', '{data['year']}', '{data['chassis_no']}');")
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as E:
        print(E.msg)
        raise E


def insertToOwner(data: dict):
    try:
        cursor.execute(f"INSERT INTO OWNER (name, address, phone) "
                       f"VALUE ('{data['name']}', '{data['address']}', '{data['phone']}');")
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as E:
        print(E.msg)
        raise E


def insertToPolicy(data: dict):
    try:
        cursor.execute(f"INSERT INTO POLICY (car_id, start_date) "
                       f"VALUE ('{data['car_id']}', '{data['start_date']}');")
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as E:
        print(E.msg)
        raise E


def insertToClaim(data: dict):
    try:
        cursor.execute(
            f"INSERT INTO CLAIM (policy_no, claim_date, workshop_id, driver_name, driver_license_no, claim_amt, status) "
            f"VALUE ({data['policy_no']}, '{data['claim_date']}', {data['workshop_id']},'{data['driver_name']}', '{data['driver_license_no']}', {data['claim_amt']}, 'PROCESSING');")
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as E:
        print(E.msg)
        raise E


def insertToWorkshop(data: dict):
    try:
        cursor.execute(
            f"INSERT INTO WORKSHOP (name, address, phone) VALUE ('{data['name']}', '{data['address']}', '{data['phone']}');")
        connection.commit()
        return cursor.lastrowid

    except mysql.connector.Error as E:
        print(E.msg)
        raise E


def askforString(columnName: str):
    res = input("Enter {}: ".format(columnName))
    if res == '':
        res = None
    return res


def askforInt(columnName: str):
    res = input("Enter {}: ".format(columnName))
    if res == '':
        res = None
    else:
        res = int(res)
    return res


# no update in car data
def get_input_car():
    stringdata = ['engine_no', 'make', 'model', 'year', 'chassis_no']
    intdata = ['owner_id']
    res = {}
    for data in stringdata:
        res[data] = askforString(data)
    for data in intdata:
        res[data] = askforInt(data)
    return res


def get_input_owner(id_required: bool):
    stringdata = ['name', 'address', 'phone']
    res = {}
    if id_required:
        res['owner_id'] = askforInt('owner_id')
    for data in stringdata:
        res[data] = askforString(data)
    return res


# no udpate in policy data
def get_input_policy(id_required: bool):
    stringdata = ['car_id', 'start_date']
    res = {}
    if id_required:
        res['policy_id'] = askforInt('policy_id')
    for data in stringdata:
        res[data] = askforString(data)
    return res


def get_input_workshop(id_required: bool):
    stringdata = ['name', 'address', 'phone']
    res = {}
    if id_required:
        res['workshop_id'] = askforInt('workshop_id')
    for data in stringdata:
        res[data] = askforString(data)
    return res


# no update in claim
def get_input_claim(id_required: bool):
    stringdata = ['claim_date', 'driver_name', 'driver_license_no']
    intdata = ['policy_no', 'workshop_id', 'claim_amt']
    res = {}
    if id_required:
        res['claim_id'] = askforInt('claim_id')
    for data in stringdata:
        res[data] = askforString(data)
    for data in intdata:
        res[data] = askforInt(data)
    return res


def update_owner():
    inp = get_input_owner(True)
    command = "UPDATE OWNER SET "
    for key, val in inp.items():
        if key != 'owner_id' and val is not None:
            command = command + f" {key} = '{val}', "
    command = command.removesuffix(', ')
    command = command + f" WHERE owner_id = {inp.get('owner_id')};"
    cursor.execute(command)
    connection.commit()


def update_workshop():
    inp = get_input_workshop(True)
    command = "UPDATE WORKSHOP SET "
    for key, val in inp.items():
        if key != 'owner_id' and val is not None:
            command = command + f"{key} = '{val}', "
    command = command.removesuffix(', ')
    command = command + f" WHERE workshop_id = {inp.get('workshop_id')};"
    cursor.execute(command)
    connection.commit()


def update_claim_status():
    cursor.execute(f"UPDATE claim SET status='PAID' WHERE claim_id={askforInt('claim id')}")
    connection.commit()


# assuming data is already selected from db
def printTable():
    print(tabulate.tabulate(fetchData(), headers='firstrow'))


def fetchData():
    datas = [cursor.column_names]
    for rows in cursor.fetchmany(10):
        row = []
        for data in rows:
            row.append(data)
        datas.append(row)
    return datas


def query_car_by_engine_no():
    cursor.execute(f"SELECT DISTINCT * FROM car WHERE engine_no = '{askforString('engine_no')}'")
    printTable()


def query_car_by_owner():
    cursor.execute(
        f"SELECT engine_no as Engine, make as Name, name as Owner FROM car NATURAL JOIN owner WHERE owner.name='{askforString('owner name')}'")
    printTable()


def query_car_by_ownerId():
    cursor.execute(
        f"SELECT engine_no as Engine, make as Name, name as Owner  FROM car NATURAL JOIN owner WHERE owner.owner_id={askforInt('owner_id')}")
    printTable()


def list_insured_car_by_owner():
    cursor.execute(
        f"SELECT c.engine_no as Engine, c.make as Name, o.name as Owner, o.address as Address, o.phone as Phone, p.policy_id as PolicyID, p.start_date as StartDate, p.end_date as EndDate FROM car c NATURAL JOIN owner o JOIN policy p on p.car_id=c.engine_no WHERE o.name='{askforString('owner name')}'")
    printTable()


def list_insured_car_by_ownerId():
    cursor.execute(
        f"SELECT c.engine_no as Engine, c.make as Name, o.name as Owner, o.address as Address, o.phone as Phone, p.policy_id as PolicyID, p.start_date as StartDate, p.end_date as EndDate FROM car c NATURAL JOIN owner o JOIN policy p on p.car_id=c.engine_no WHERE o.owner_id='{askforInt('owner id')}'")
    printTable()


def show_claim_status():
    cursor.execute(f"SELECT * FROM claim WHERE claim_id={askforInt('claim id')}")
    printTable()


def work():
    while True:
        try:
            oper: int = int(input("Enter the operation number:\n"
                                  "1. Insert\n"
                                  "2. Update\n"
                                  "3. Query\n"
                                  "4. Exit\n"
                                  "::"))
            if oper == 1:
                oper = int(input(
                    "Enter the table you want to insert to:\n"
                    "1. Car\n"
                    "2. Owners\n"
                    "3. Workshop\n"
                    "4. Policy\n"
                    "5. Claim\n"
                    "::"))
                if oper == 1:
                    datas = get_input_car()
                    insertToCar(datas)
                    print(f"Car added to table")
                elif oper == 2:
                    datas = get_input_owner(False)
                    id_num = insertToOwner(datas)
                    print(f"Person added to the table with id {id_num}")
                elif oper == 3:
                    datas = get_input_workshop(False)
                    id_num = insertToWorkshop(datas)
                    print(f"Workshop added to the table with id {id_num}")
                elif oper == 4:
                    datas = get_input_policy(False)
                    id_num = insertToPolicy(datas)
                    print(f"Car insured with policy number {id_num}")
                elif oper == 5:
                    datas = get_input_claim(False)
                    id_num = insertToClaim(datas)
                    print(f"Claim request initiated with token number {id_num}")
                else:
                    print("Error! Unexpected value")
            elif oper == 2:
                oper = int(input("Enter the table you want to update: \n"
                                 "1. Owner\n"
                                 "2. Workshop\n"
                                 "3. Claim\n"
                                 "::"))
                print("Note: Leave empty if you do not want to update the value:")
                if oper == 1:
                    update_owner()
                    print("Owner data updated successfully")
                elif oper == 2:
                    update_workshop()
                    print("Workshop data updated successfully")
                elif oper == 3:
                    update_claim_status()
                    print("Claim status changed successfully")
                else:
                    print("Error! Unexpected value")
            elif oper == 3:
                oper = int(input("Enter the query you want to execute:\n"
                                 "1. Search car by engine number:\n"
                                 "2. Search car by owner name:\n"
                                 "3. Search car by owner id:\n"
                                 "4. Search insured car by owner name:\n"
                                 "5. Search insured car by owner id:\n"
                                 "6. Show Claim status by id\n"
                                 "::"))
                if oper == 1:
                    query_car_by_engine_no()
                elif oper == 2:
                    query_car_by_owner()
                elif oper == 3:
                    query_car_by_ownerId()
                elif oper == 4:
                    list_insured_car_by_owner()
                elif oper == 5:
                    list_insured_car_by_ownerId()
                elif oper == 6:
                    show_claim_status()
            elif oper == 4:
                break
            else:
                print("Error! Unexpected value")
        except mysql.connector.Error as e:
            print(e.msg)
        except Exception as e:
            print(e)
        print("\n")


try:
    connection = mysql.connector.connect(
        user='',# user id and password of mysql 
        password='',
        host='127.0.0.1',
        database='CarInsurance'
    )
    print(connection)
    DB_NAME = 'CarInsurance'
    cursor = connection.cursor()
    try:
        cursor.execute(f"USE {DB_NAME}")
        print(f"Connected to Database {DB_NAME}")
    except mysql.connector.Error as err:
        print(err.msg)


    work()
    cursor.close()
    connection.close()
except mysql.connector.Error as err:
    print(err.msg)
