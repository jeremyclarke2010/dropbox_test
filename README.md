# dropbox_test

## Install support libraries
This application was developed with Python v3.8.2
```
pip install pyinstaller
pip install dirsync
pip install --user pyinputplus
pip install pytest
```

## Checkout Code
Using git command
```
git clone https://github.com/Amy-TestHub/dropbox_test.git
```

## Create executable file
From 'dropbox_test' root directory
```
pyinstaller --onefile syncfolder/sync_folder.py
```
Compiled program stores in: **dropbox_test/dist/sync_folder**


## Running the program
From 'dropbox_test' root directory
### Run as CLI program
```
./dist/sync_folder
```
# Run as Python program
```
python3 syncfolder/sync_folder.py
```

## Input arguments
- Source directory (client)
- Destination directory (server)
- Enable file deduplication? Yes/No
- If file deduplication is enabled, set a threshold between 0 and 100 (e.g. when threshold is set to 50, if file shares over 50% of same content with another file, this file will not be uploaded)

### Examples
- Sync whole repository without file deduplication: 
```
Please enter source directory: /client
Please enter destination directory: /server
Enable same partial file deduplication? yes/no: no
```
- Ignore file has identical content for upload: 
```
Please enter source directory: /client
Please enter destination directory: /server
Enable same partial file deduplication? yes/no: yes
Please enter same partial file threshold, between 0 and 100: 100
```
- Ignore file has over 50% same contents with another file:
```
Please enter source directory: /client
Please enter destination directory: /server
Enable same partial file deduplication? yes/no: yes
Please enter same partial file threshold, between 0 and 100: 50
```
**WARNING**: Ignored fill will be renamed with _ignore suffix

### Sync with network drive
Map the network drive to a local folder, ensure using the correct path
e.g. '/Volumes/Shared Folder' is a mapped network drive on local Mac machine

# Run PyTest module
Tests are created using PyTest Framework, test steps generally following below steps:
- Create a new **client** folder, copy test files into the folder
- Mock CLI input arguments by setting up variables
- Running sync folder function, upload selected files to **server** folder
- Validate files uploaded on the server side
- Tear down tests, remove client and server folder created by the script
```
pytest syncfolder/test_sync_folder.py
```

# Future enhancement
- Improve the logic to ignore duplicate file upload WITHOUT rename the original file
- Implement a environment requirement setup file
- Expand testing to include multiple file types and file permission testing