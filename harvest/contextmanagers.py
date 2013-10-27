import os

class cd(object):
    "Context manager for changing the current working directory."
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.current = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, exception, value, traceback):
        os.chdir(self.current)
