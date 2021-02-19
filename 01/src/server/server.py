"""
 Implements a simple HTTP/1.0 Server
"""
import json
import socket
import pymongo


# Define socket host and port
from pymongo.cursor import Cursor

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'ddw'

client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db]

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # tags: list = list(db['tags'].find({"y": {"$gte": 0.2}}, {"_id": 0, "label": 1, "y": 1}))
    tags: list = list(db['tags'].find({}, {"_id": 0, "label": 1, "y": 1}).sort("y", -1).limit(10))

    # Send HTTP response
    response = "HTTP/1.1 200 OK\n"\
               + "Content-Type: text/json\n"\
               + "Access-Control-Allow-Origin: *\n"\
               + "\n"\
               + json.dumps(tags)\
               + '\n'
    client_connection.sendall(response.encode())
    client_connection.close()
