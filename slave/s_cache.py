import socket
import json
import sqlite3
import os
import requests

# service setup 
HOST_NAME = "127.0.0.1"
PORT_NUMBER = int(os.getenv('PORT'))
GATEWAY_HOST = os.getenv('GATEWAYHOST')

GATEWAY_PORT = int(os.getenv('GATEWAYPORT'))

BUFFER_SIZE = 1024
ENDPOINT_SLAVE = '/register/cache'

print(PORT_NUMBER)

def register(GATEWAY_HOST, GATEWAY_PORT, HOST_NAME, PORT_NUMBER, ENDPOINT):
    jsonData = json.dumps({ 'HOST': HOST_NAME, 'PORT': PORT_NUMBER })
    print(jsonData)
    requests.post('http://' + GATEWAY_HOST+':' + str(GATEWAY_PORT) + ENDPOINT, data=jsonData, headers={'Connection':'close'})

register(GATEWAY_HOST, GATEWAY_PORT, HOST_NAME, PORT_NUMBER, ENDPOINT_SLAVE)

# example JSON 
# {"expects": "users", "id": 5}
# {"id": 1, "userId": 2, "type": "some type", "cost": 10000}
# {"id": "4", "firstName": "Liza", "lastName": "G", "email": "vasea@gmail.com", "birthDate": "2020-10-10"}

def check_data(response):
    if "expects" in json.loads(response):
        return send_cached_data(response)
    else: return save_JSON(response)

# SAVE JSON TO SQLITE DB

def save_JSON(response):
    resp = json.loads(response)

    values = list()
    i = 0
    for k, v in resp.items():
        values.insert(i, v)
        i = i + 1
    values = tuple(values)
    if "firstName" in resp:
        sql = ''' INSERT INTO users VALUES(?,?,?,?,?) '''
    else: sql = ''' INSERT INTO insurances VALUES(?,?,?,?) '''
    
    try:
        conn = sqlite3.connect("../db") 
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
    
    except: return '{"message": "fail"}'

    return '{"message": "success"}'

# SQLITE TO JSON

def send_cached_data(response): 
    data = json.loads(response)
    table_name = data["expects"]
    data_id = data["id"] 
    print(table_name)
    
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn = sqlite3.connect("../db")
    conn.row_factory = dict_factory
    cur1 = conn.cursor()
    
    cur1.execute("SELECT * FROM " + table_name + " WHERE id = " + str(data_id) + ";")
     
    results = cur1.fetchall()
    if results == []:
        return '{"message": "no data"}'
    else: return json.dumps(results)
    
# CONNECTION 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST_NAME, PORT_NUMBER))
s.listen(1)

conn, addr = s.accept()
print("Connection address: ", addr)
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("Received data:", data)
    response = check_data(data)
    # print(response)
    conn.send(str.encode(response))