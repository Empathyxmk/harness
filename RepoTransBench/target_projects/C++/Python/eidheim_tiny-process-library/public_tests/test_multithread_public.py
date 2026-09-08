import subprocess
import threading

def test_parallel_echoes():
    num_threads = 3
    inputs = ["peach", "grape", "melon"]
    outputs = [""] * num_threads
    threads = []

    def make_thread(i):
        def fn():
            proc = subprocess.Popen(['cat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, _ = proc.communicate(input=inputs[i].encode())
            outputs[i] = out.decode()
        return fn

    for i in range(num_threads):
        t = threading.Thread(target=make_thread(i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    for i in range(num_threads):
        assert outputs[i] == inputs[i]

def test_multiple_patterns_grep():
    num_threads = 3
    inputs = [
        "aa\nbb\ncc\n",
        "xx\nyy\n",
        "green\nyellow\n"
    ]
    patterns = ["cc", "yy", "yellow"]
    expected = ["cc\n", "yy\n", "yellow\n"]
    outputs = [""] * num_threads
    threads = []

    def make_thread(i):
        def fn():
            proc = subprocess.Popen(['grep', patterns[i]], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, _ = proc.communicate(input=inputs[i].encode())
            outputs[i] = out.decode()
        return fn

    for i in range(num_threads):
        t = threading.Thread(target=make_thread(i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    for i in range(num_threads):
        assert outputs[i] == expected[i]