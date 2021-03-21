import socket
import os
import time


class Client:
    def client_config(self):
        # Set source folder
        while True:
            self.source = input("Source folder: ")
            if(os.path.exists(self.source)):
                break
            else:
                print("Invalid file path!")
        
        # Set server ip and port
        self.ip = input('Enter server ip: ')
        self.port = int(input('Enter server port: '))

    def connect_server(self):
        # Establish connection to server
        self.s = socket.socket()
        self.s.connect((self.ip, self.port))

    def init_upload(self):
        file_list = os.listdir(self.source)
        self.add_files(file_list)
        # Initialte synced_files list
        self.synced_files = {}
        for f in file_list:
            path = os.path.join(self.source, f)
            timestamp = os.path.getmtime(path)
            self.synced_files[f] = timestamp

    def add_files(self, file_list):
        for file in file_list:
            # Sending file name to server
            self.s.send(file.encode())
            print(self.s.recv(1024).decode())

            # Sending request type to server
            self.s.send("add".encode())
            print(self.s.recv(1024).decode())

            # Sending file data to server
            file_path = os.path.join(self.source, file)
            with open(file_path, "rb") as f:
                while True:
                    file_data = f.read(1024)
                    if file_data == b'':
                        break
                    self.s.send(file_data)
            print("Sending file completed: ", file)

            # Start new thread for each file
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            self.connect_server()

    def delete_files(self, file_list):
        for file in file_list:
            # Sending file name to server
            self.s.send(file.encode())
            print(self.s.recv(1024).decode())

            # Sending request type to server
            self.s.send("delete".encode())
            print(self.s.recv(1024).decode())
            print("Deleting file completed: ", file)

            # Start new thread for each file
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            self.connect_server()

    def check_update(self):
        # Get current local file list
        self.local_files = {}
        files = os.listdir(self.source)
        for f in files:
            path = os.path.join(self.source, f)
            timestamp = os.path.getmtime(path)
            self.local_files[f] = timestamp

        # Check for add/update file
        to_add = []
        for i in self.local_files:
            if i in self.synced_files:
                # Compare timestamp
                if (self.synced_files[i] != self.local_files[i]):
                    to_add.append(i)
            else:
                to_add.append(i)
        if len(to_add) > 0:
            print("File to add/update: ", to_add)
        self.add_files(to_add)

        # Check for delete file
        to_delete = []
        for i in self.synced_files:
            if i not in self.local_files:
                to_delete.append(i)
        if len(to_delete) > 0:
            print("File to delete: ", to_delete)
        self.delete_files(to_delete)

        # Rebase synced file list
        self.synced_files = self.local_files

if __name__ == "__main__":
    client = Client()
    client.client_config()
    client.connect_server()
    client.init_upload()
    # Monitoring changes with 10s intervals
    while True:
        client.check_update()
        time.sleep(10)
