import os
import sys

def running_models():
    import psutil
    procs = []
    for p in psutil.process_iter(['cmdline', 'environ']):
        try:
            env = p.environ()
            if any("/models--" in v for v in env.values()):
                procs.append(p)
        except Exception:
            continue
    return procs