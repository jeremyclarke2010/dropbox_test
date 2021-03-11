import pytest
import shutil
from os import walk
from sync_folder import SyncFolder

@pytest.fixture
def sync_dir():
    # Mock cmd line arguments
    testdata_dir = "testdata"
    source_dir = "client"
    dest_dir = "server"
    shutil.copytree(testdata_dir,source_dir)
    return source_dir, dest_dir

def test_no_dedupe(sync_dir):
    enable_dedupe = "no"
    sync_job = SyncFolder(sync_dir[0],sync_dir[1],enable_dedupe)
    sync_job.sync_folder()


def test_dedupe_100(sync_dir):
    enable_dedupe = "yes"
    sync_job = SyncFolder(sync_dir[0],sync_dir[1],enable_dedupe)
    sync_job.threshold = 100
    sync_job.dedupe_files()
    sync_job.sync_folder()
    # Validate files in server
    file_list = []
    for (dirpath, dirnames, filenames) in walk(self.source_dir):
        file_path = (path.join(dirpath, file) for file in filenames)
        file_list.extend(file_path)
    print(file_list)