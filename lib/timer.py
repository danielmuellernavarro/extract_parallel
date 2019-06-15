import time


def timer(f):
    def wrapper(*args, **kwargs):
        try:
            t0 = time.time()
            print('File: \"{0}\" extracting'.format(args[0]))
            return f(*args, **kwargs)
        finally:
            t1 = time.time()
            print('File: \"{0}\" extracted. It took {1:.3} seconds\n'.format(args[0], t1 - t0))
    return wrapper
