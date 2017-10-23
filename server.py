# Author: Gregory Bushnell
# Class: Adv Robotics Final Project.
# Server code to recive data from client 

from socket import *

server = socket(AF_INET, SOCK_STREAM)
host = ""
port = 5150
server.bind((host, port))
#server.settimeout(5.0)
print("Listening...")
server.listen(5)
clients = []
client_data={0:[],
             1:[]
             }
i=0
done=[False,False]


while i<1:
    (client, addr) = server.accept()
    client.settimeout(4.0)
    print("Client accepted from: ", addr)
    clients.append(client)
    clients[i].send(str.encode("start"))
    i+=1
j=0
text=""
while not all(done):
    try:
        data = clients[j%1].recv(1024)
        text = bytes.decode(data)
        client_data[j%1].append(text)
        #print("data:", text)
    except Exception as e:
        print("No data")
        #print(e)
        continue
    finally:
        j+=1
    if text == "finish":
        done[j%1]=True
        break
 
    
print("Client 1 dtata: ",client_data[0])
print("Client 2 data: ",client_data[1])
client.close()
server.close()
