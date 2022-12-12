import time
from functools import wraps
import hashlib
import itertools
from typing import List, Callable

# https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator
def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        print(f'Enter: {f.__name__}()...') # {args},{kw} has too much data
        result = f(*args, **kw)
        te = time.time()
        # print f'func:%r args:[%r, %r] took: %2.4f sec' % \
        #   (f.__name__, args, kw, te-ts)
        print(f'Finished: {f.__name__} took {te-ts} sec')
        return result
    return wrap


def hash_sha256(s: str) -> str:
    return hash_bytes(s).hex()


def hash_bytes(s: str) -> bytes:
    """
    Convert a hex string to bytes
    > bytes.fromhex(my_hex_string)

    Convert bytes to a hex string
    > my_bytes.hex()
    
    """
    return hashlib.sha256(s.encode('utf-8')).digest()


def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


def remove_duplicates(xs: List, key: Callable) -> List:
    """
    Remove duplicates from a list of objects.
    https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
    """
    seen = set()
    return [x for x in xs if not (key(x) in seen or seen.add(key(x)))]