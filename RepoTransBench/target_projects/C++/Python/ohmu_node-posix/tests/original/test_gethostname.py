import os
from posix_py import gethostname

def test_gethostname():
    hostname = gethostname()
    print("hostname:", hostname)
    assert hostname == os.uname().nodename or hostname == os.uname().sysname