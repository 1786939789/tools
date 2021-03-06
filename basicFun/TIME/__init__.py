import time
class Task():  
    def __init__(self, prefix=None):
        self.prefix = prefix + ' ' if prefix else 'Unnamed task'
    def __enter__(self):
        self.start = time.time()
    def __exit__(self, *args):
        print('%stime: %.4f sec' % (self.prefix, time.time() - self.start))