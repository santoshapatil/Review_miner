import time

def start_time():
    start=time.time()
    return start 

def log_time(start):
    diff=time.time()-start
    return diff
