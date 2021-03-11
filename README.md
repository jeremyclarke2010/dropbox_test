# dropbox_test

## Install Python and dependencies
This application is developed with Python v3.8.2
# Application dependencies
pip install pyinstaller
pip install dirsync
pip install --user pyinputplus
# PyTest dependencies
pip install pytest
pip install cli-test-helpers

## Code function

## Create executable file
pyinstaller --onefile sync_folder.py
Package your entire application into a single executable file.


## Running the application
# Run execuatble
/Users/hongyingzhao/TestAutomation/dropbox_test/dist/sync_folder
# Run as Python programe
cd ./dropbox_test
python3 syncfolder/sync_folder.py 

# Input arguments

testdata/client
testdata/server

<!-- source_dir = '/Users/hongyingzhao/Desktop/To Share'
dest_dir = '/Volumes/Shared Folder' -->


# Run PyTest module