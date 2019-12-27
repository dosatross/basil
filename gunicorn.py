bind = "0.0.0.0:8000"

workers = 1
from multiprocessing import cpu_count
try:
    workers = cpu_count() + 1
except NotImplementedError:
    pass

worker_class = "sync"

accesslog = '-' 