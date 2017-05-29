# Variable used for locking system resources by variables
LOCK = None


def init_locks(l):
    global LOCK
    LOCK = l
