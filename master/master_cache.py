import socket
import json
import sqlite3
import os
import requests

def register(GATEWAY_HOST, GATEWAY_PORT, HOST_NAME, PORT_NUMBER, ENDPOINT):
    jsonData = json.dumps({ 'host': HOST_NAME, 'port': PORT_NUMBER })
    print(jsonData)
    try:
        requests.post('http://' + GATEWAY_HOST+':' + str(GATEWAY_PORT) + ENDPOINT, data=jsonData)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"

def send_data_to_Slave(response):
    for port in SLAVE_PORTS:
        addr2 = 0
        while (addr2 != port):
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.bind((HOST_NAME, PORT_NUMBER))
            s2.listen(1)
            conn2, addr2 = s.accept()
        conn2.send(response)

HOST_NAME = "127.0.0.1"
PORT_NUMBER = int(os.getenv('PORT'))
GATEWAY_HOST = os.getenv('GATEWAYHOST')
print(PORT_NUMBER)
GATEWAY_PORT = int(os.getenv('GATEWAYPORT'))
ENDPOINT_MASTER = '/register/cache/master'

register(GATEWAY_HOST, GATEWAY_PORT, HOST_NAME, PORT_NUMBER, ENDPOINT_MASTER)

SLAVE_PORTS = [5009, 5010]

#connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST_NAME, PORT_NUMBER))
s.listen(1)

conn, addr = s.accept()
print("Connection address: ", addr)
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("Received data:", data)
    send_data_to_Slave(data)
    # print(response)
    conn.send(str.encode(response))