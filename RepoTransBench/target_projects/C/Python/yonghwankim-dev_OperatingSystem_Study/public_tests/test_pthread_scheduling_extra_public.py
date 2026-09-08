import threading
import time

def public_test_extra_func(arg):
    arg[0] = arg[0] * 3
    # Simulate a small delay
    time.sleep(0.005)

def test_scheduling_thread3_public():
    a, b, c = [2], [4], [8]
    t1 = threading.Thread(target=public_test_extra_func, args=(a,))
    t2 = threading.Thread(target=public_test_extra_func, args=(b,))
    t3 = threading.Thread(target=public_test_extra_func, args=(c,))
    t1.start(); t2.start(); t3.start()
    t1.join(); t2.join(); t3.join()
    assert a[0] == 6  # 2*3
    assert b[0] == 12
    assert c[0] == 24

def test_scheduling_thread4_public():
    a, b, c, d = [5], [6], [7], [8]
    t1 = threading.Thread(target=public_test_extra_func, args=(a,))
    t2 = threading.Thread(target=public_test_extra_func, args=(b,))
    t3 = threading.Thread(target=public_test_extra_func, args=(c,))
    t4 = threading.Thread(target=public_test_extra_func, args=(d,))
    t1.start(); t2.start(); t3.start(); t4.start()
    t1.join(); t2.join(); t3.join(); t4.join()
    assert a[0] == 15
    assert b[0] == 18
    assert c[0] == 21
    assert d[0] == 24