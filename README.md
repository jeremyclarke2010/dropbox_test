# dropbox_test
Simple server - client type file syncing Python program, the synchronise is from client to server only

## Checkout code
```
git clone https://github.com/Amy-TestHub/dropbox_test.git
```
## Assumptions
- Both server and client are on the same network, or have public IP address
- There is no router, firewall rule configured
- Both source and destination folder has public right to read and write

## Running server
Open executables in **dist** directory
```
./dist/server
```
Enter an existing destination directory for files to sync to
```
Destination folder: 
```
Enter a port number that server will listening on
```
Enter port number:
```
You shall see similar to below:
```
Server will listen on 192.168.16.10: 8080
Waiting for connection ... 
```

## Running client
Open executables in **dist** directory
```
./dist/client
```
Enter an existing source directory to sync with
```
Source folder: 
```
Enter server IP address, that displayed on server side
```
Enter server IP:
```
Enter server port, that displayed on server side
```
Enter server port:
```
You shall see similar to below:
```
Syncing file to server ...
```
Followed by any file in source folder will be send to server
```
Sending file completed:  test1.txt
Syncing file to server ...
Sending file completed:  test2.txt
Syncing file to server ...
```

## Exiting program
Client will sync with server every 10s. 
Both server and client will run until terminated by user

## Future enhancement
- Enable server to client sync 
- Doesn't sync files in sub-directories from the source folder
- Image sync is flaky
