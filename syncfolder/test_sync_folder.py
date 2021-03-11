import pytest
import shutil
from os import walk,path
from sync_folder import SyncFolder

@pytest.fixture
def sync_dir(request):
    # Mock cmd line arguments
    testdata_dir = "testdata"
    source_dir = "client"
    dest_dir = "server"
    shutil.copytree(testdata_dir,source_dir)
    yield source_dir, dest_dir
    # Tear down after script
    shutil.rmtree("client")
    shutil.rmtree("server")

def test_no_dedupe(sync_dir):
    enable_dedupe = "no"
    sync_job = SyncFolder(sync_dir[0],sync_dir[1],enable_dedupe)
    sync_job.sync_folder()
    # Validate files in server
    assert(path.exists('server/test1_copy.txt'))
    assert(path.exists('server/test1.txt'))
    assert(path.exists('server/test2_partial.txt'))
    assert(path.exists('server/test2.txt'))
    assert(path.exists('server/sub_dir/test3.txt'))

def test_dedupe_0(sync_dir):
    enable_dedupe = "yes"
    sync_job = SyncFolder(sync_dir[0],sync_dir[1],enable_dedupe)
    sync_job.threshold = 0
    sync_job.dedupe_files()
    sync_job.sync_folder()
    # Validate files in server
    assert(path.exists('server/test1_copy.txt') == False)
    assert(path.exists('server/test1.txt')) # The first file will be synced
    assert(path.exists('server/test2_partial.txt') == False)
    assert(path.exists('server/test2.txt') == False)
    assert(path.exists('server/sub_dir/test3.txt') == False)

def test_dedupe_50(sync_dir):
    enable_dedupe = "yes"
    sync_job = SyncFolder(sync_dir[0],sync_dir[1],enable_dedupe)
    sync_job.threshold = 50
    sync_job.dedupe_files()
    sync_job.sync_folder()
    # Validate files in server
    assert(path.exists('server/test1_copy.txt') == False)
    assert(path.exists('server/test1.txt'))
    assert(path.exists('server/test2_partial.txt') == False)
    assert(path.exists('server/test2.txt'))
    assert(path.exists('server/sub_dir/test3.txt'))

def test_dedupe_100(sync_dir):
    enable_dedupe = "yes"
    sync_job = SyncFolder(sync_dir[0],sync_dir[1],enable_dedupe)
    sync_job.threshold = 100
    sync_job.dedupe_files()
    sync_job.sync_folder()
    # Validate files in server
    assert(path.exists('server/test1_copy.txt') == False)
    assert(path.exists('server/test1.txt'))
    assert(path.exists('server/test2_partial.txt'))
    assert(path.exists('server/test2.txt'))
    assert(path.exists('server/sub_dir/test3.txt'))