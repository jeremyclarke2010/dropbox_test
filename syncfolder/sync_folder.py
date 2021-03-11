import pyinputplus
from os import walk, path, rename
from difflib import SequenceMatcher
from dirsync import sync
import time

class SyncFolder:

    def __init__(self,source_dir,dest_dir,enable_dedupe):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.enable_dedupe = enable_dedupe
    
    def set_threshold(self):
        while True:
            self.threshold = pyinputplus.inputNum('Please enter same partial file threshold, between 0 and 100: ')
            if self.threshold<0 or self.threshold>100:
                print('Please enter a number between 0 and 100')
                continue
            break
        return self.threshold

    def dedupe_files(self):
        # Get all files from source directory, include sub directories
        file_list = []
        for (dirpath, dirnames, filenames) in walk(self.source_dir):
            file_path = (path.join(dirpath, file) for file in filenames)
            file_list.extend(file_path)

        # Deduplicate files, ignore file with patially same contents over the threshold
        unique_files = []
        for filename in file_list:
            for item in unique_files:
                # Check for files duplicate ratio
                file1 = open(filename,'rb').read()
                file2 = open(item,'rb').read()
                same_ratio = SequenceMatcher(None, file1, file2).ratio()
                same_ratio = round(same_ratio*100,2)
                # Tag files over threshold
                if same_ratio >= self.threshold:
                    rename(filename,filename+"_ignore")
                    break
            else:
                unique_files.append(filename)
        return unique_files

    # Sync folder, ignore same patial files
    def sync_folder(self):
        pattern = ('^.*_ignore$',)
        sync(self.source_dir, self.dest_dir, 'sync', create = True, purge = True, content = True, ignore = pattern)

if __name__ == "__main__":
    # Input arguments from run time
    source_dir = pyinputplus.inputFilepath('Please enter source directory: ',mustExist=True)
    dest_dir = pyinputplus.inputFilepath('Please enter destination directory: ',mustExist=True)
    enable_dedupe = pyinputplus.inputYesNo('Enable same partial file deduplication? yes/no: ')
    # Sync folders
    sync_job = SyncFolder(source_dir,dest_dir,enable_dedupe)
    if enable_dedupe == 'yes':
        sync_job.set_threshold() # Set threshold for dedupe
        sync_job.dedupe_files()
    while True:
        sync_job.sync_folder()
        time.sleep(10)