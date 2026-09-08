# hamms/__init__.py
class HammsServer:
    def __init__(self):
        self.running = False
    def start(self):
        self.running = True
        print("HammsServer started")
    def stop(self):
        self.running = False
        print("HammsServer stopped")