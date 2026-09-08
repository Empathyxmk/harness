"""
Example of how to run the Hamms Server from running Python code instead of the
command line.
"""
from hamms import HammsServer

def run_thread_example():
    hs = HammsServer()
    hs.start()
    print("stopping")
    hs.stop()

if __name__ == '__main__':
    run_thread_example()