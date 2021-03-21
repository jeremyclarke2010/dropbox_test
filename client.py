import socket
import os
import time


class Client:
    def client_config(self):
        # Set source folder
        self.source = "./client" #DEBUG
        # while True:
        #     self.source = input("Source folder: ")
        #     if(os.path.exists(self.source)):
        #         break
        #     else:
        #         print("Invalid file path!")
        # Set server ip and port
        self.ip = "192.168.86.20" #DEBUG
        self.port = int(8080) #DEBUG
        # self.ip = input('Enter server ip: ')
        # self.port = int(input('Enter server port: '))

    def connect_server(self):
        # Establish connection to server
        self.s = socket.socket()
        self.s.connect((self.ip, self.port))
        # print(self.s.recv(1024).decode())

    def init_upload(self):
        # print("Sending file from client ...")

        file_list = os.listdir(self.source)
        for file in file_list:

            # print("File name: ", file)
            self.s.send(file.encode())
            print(self.s.recv(1024).decode())

            file_path = os.path.join(self.source, file)
            # print("File path: ", file_path)

            # with open(file_path, "rb") as f:
            #     file_data = f.read(2097152) # 2MB
            #     # print("Send data: ", file_data)
            #     self.s.send(file_data)
            # print("Sending file completed: ",file)

            with open(file_path, "rb") as f:
                while True:
                    file_data = f.read(1024)
                    # print("Data batch: ",file_data)
                    
                    if file_data == b'':
                        break
                    self.s.send(file_data)
                print("Sending file completed: ",file)

            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            self.connect_server()

def check_update(dir):
    files = os.listdir(dir)
    for f in files:
        size = os.path.getsize(dir+f)
        time = os.path.getmtime(dir+f)
        print(f"File {f} size is {size}, last modified at : {time}")

# 192.168.86.20

if __name__ == "__main__":
    client = Client()
    client.client_config()
    client.connect_server()
    client.init_upload()
    # while True:
    # check_update("./syncfolder/client/")
    # client.send_update()
