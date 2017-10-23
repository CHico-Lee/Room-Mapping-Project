# Author: Gregory Bushnell
# Class: Adv Robotics Final Project.
# client code to send data to server.  

from socket import *

def connect():
    server = socket(AF_INET, SOCK_STREAM)
    host = "10.10.0.116"
    port = 5151
    server.connect((host, port))
    return server

def send_data(server, data):
    data_str = str.encode(data)
    #data_str = str(data).encode()
    server.send(data_str)
    
def recv_data(server):
    data = server.recv(1024)
    data_text = bytes.decode(data)
    return data_text

def disconnect(server):
    server.close()
