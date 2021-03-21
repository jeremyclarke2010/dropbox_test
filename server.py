import socket
import os
import time
import threading


class Server:
    def server_config(self):
        # Set destination folder
        self.dest = "./server"  # DEBUG
        # while True:
        #     self.dest = input("Destination folder: ")
        #     if(os.path.exists(self.dest)):
        #         break
        #     else:
        #         print("Invalid file path!")
        # Get server ip from system
        self.ip = socket.gethostbyname(socket.gethostname())
        # Set port number for server to listen on
        self.port = int(8080)  # DEBUG
        # while True:
        #     try:
        #         self.port = int(input("Enter port number: "))
        #         if self.port in range(0, 65353):
        #             break
        #     except ValueError:
        #         print("Invalid port number!")
        print(f"Server will listen on {self.ip}: {self.port}")

    def connect_client(self):
        # Enable listening on server
        self.s = socket.socket()
        self.s.bind((self.ip, self.port))
        self.s.listen(10)
        print("Waiting for connection ... ")

    def sync_folder(self):
        while True:
            # Establish client connetion
            self.c, self.addr = self.s.accept()
            # print(self.addr, " is connected")
            # self.c.send("Connected to server".encode())
            # Sync folder
            threading.Thread(target=self.add_files).start()

    def add_files(self):
        # print("Syncing file to server ...")

        # while True:

        file_name = self.c.recv(1024).decode()
        # print("File name: ", file_name)
        self.c.send(f"Sync file {file_name} to server.".encode())

        file_path = os.path.join(self.dest, file_name)
        # print("File path: ", file_path)

        if os.path.isdir(file_path):
            print(file_path, " is a directoty, ignore")
            return

        # with open(file_path, "wb") as f:
        #     file_data = self.c.recv(2097152)  # 2MB
        #     # print("Received data: ", file_data)
        #     f.write(file_data)
        #     f.close()
        #     print("Receiving file completed: ", file_name)

        with open(file_path, "wb") as f:
            while True:
                file_data = self.c.recv(1024)
                # print("Data batch: ", file_data)
                if file_data == b'':
                    # print("break loop")
                    break
                f.write(file_data)
            f.close()
        print("Receiving file completed: ", file_name)



if __name__ == "__main__":
    server = Server()
    server.server_config()
    server.connect_client()
    while True:
        server.sync_folder()
        time.sleep(10)
