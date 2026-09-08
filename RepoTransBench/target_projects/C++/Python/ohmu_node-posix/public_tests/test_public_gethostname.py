import os
from posix_py import gethostname

def test_public_gethostname():
    hostname = gethostname()
    print("public hostname:", hostname)
    assert isinstance(hostname, str)
    assert hostname != ""
    assert hostname == os.uname().nodename