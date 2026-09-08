import subprocess
import sys
import threading

def run_and_check(ct, c, results, idx, stdout_error, exit_status_error):
    # Outputs in each thread
    cmd = f"echo Hello World {c} {ct}"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    decoded = out.decode(errors="replace")
    expected = f"Hello World {c} {ct}\n"
    if decoded != expected:
        stdout_error[idx] = True
    if proc.returncode != 0:
        exit_status_error[idx] = True

def test_multithreaded_echo():
    import time
    NUM_THREADS = 4
    ITERS = 2500
    results = [None for _ in range(NUM_THREADS)]
    stdout_error = [False] * NUM_THREADS
    exit_status_error = [False] * NUM_THREADS
    threads = []
    for ct in range(NUM_THREADS):
        def thread_fn(thread_idx=ct):
            for c in range(ITERS):
                run_and_check(thread_idx, c, results, thread_idx, stdout_error, exit_status_error)
                if stdout_error[thread_idx] or exit_status_error[thread_idx]:
                    break
        t = threading.Thread(target=thread_fn)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    if any(stdout_error):
        print("Wrong output to stdout.")
        assert False
    if any(exit_status_error):
        print("Process returned failure.")
        assert False