import threading

def thread_test_args_pub(aArg):
    return aArg

def test_thread_arg_and_retval_pub():
    ids = [101, 202, 303]
    N = len(ids)
    retvals = [None]*N
    def f(idx):
        retvals[idx] = thread_test_args_pub(ids[idx])
    threads = []
    for i in range(N):
        t = threading.Thread(target=f, args=(i,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    for i in range(N):
        assert retvals[i] == ids[i]

def test_thread_local_storage_pub():
    gLocalVar_pub = [1234]

    def target():
        gLocalVar_pub[0] = 44
    t = threading.Thread(target=target)
    t.start()
    t.join()

    assert gLocalVar_pub[0] == 1234