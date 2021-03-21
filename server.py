import socket
import os
import threading


class Server:
    def server_config(self):
        # Set destination folder
        while True:
            self.dest = input("Destination folder: ")
            if(os.path.exists(self.dest)):
                break
            else:
                print("Invalid file path!")
        
        # Get server ip from system
        self.ip = socket.gethostbyname(socket.gethostname())
        
        # Set port number for server to listen on
        while True:
            try:
                self.port = int(input("Enter port number: "))
                if self.port in range(0, 65353):
                    break
            except ValueError:
                print("Invalid port number!")
        print(f"Server will listen on {self.ip}: {self.port}")

    def connect_client(self):
        # Enable listening on server
        self.s = socket.socket()
        self.s.bind((self.ip, self.port))
        self.s.listen(10)
        print("Waiting for connection ... ")

    def sync_folder(self):
        # Establish client connetion and sync folder
        while True:
            self.c, self.addr = self.s.accept()
            threading.Thread(target=self.sync_files).start()

    def sync_files(self):
        # Receving file name from client
        file_name = self.c.recv(1024).decode()
        self.c.send(f"Syncing file to server ...".encode())
        
        # Validate file name
        file_path = os.path.join(self.dest, file_name)
        if os.path.isdir(file_path):
            return
        
        # Receiving request type from client
        try:
            sync_type = self.c.recv(1024).decode()
            self.c.send(f"{sync_type} file {file_name}".encode())
            if sync_type == "add":
                # Adding file to server
                with open(file_path, "wb") as f:
                    while True:
                        file_data = self.c.recv(1024)
                        if file_data == b'':
                            break
                        f.write(file_data)
                    f.close()
                print("Receiving file completed: ", file_name)
                return
            elif sync_type == "delete":
                # Deleting file from server
                os.remove(file_path)
                print("Deleting file completed: ",file_name)
                return
            else:
                print("Invalid sync type")
                return
        except ValueError:
            return

if __name__ == "__main__":
    server = Server()
    server.server_config()
    server.connect_client()
    while True:
        server.sync_folder()


