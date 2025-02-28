import os


from filelock import FileLock


class Lock:
    @property
    def lock(self):
        if self._lock is None:
            path = os.path.join(os.path.dirname(__file__), 'locks')
            if not os.path.exists(path):
                os.makedirs(path)
            path = os.path.join(path, f'{self.name}.lock')
            self._lock = FileLock(path)

        return self._lock

    @property
    def name(self):
        return self._name

    def __init__(self, name):
        self._name = name
        self._lock = None

    def acquire(self, timeout=None, poll_interval=None, poll_intervall=None,
                blocking=None):

        self.lock.acquire(
            timeout=timeout,
            poll_interval=poll_interval,
            poll_intervall=poll_intervall,
            blocking=blocking
        )

    def release(self, force=None):
        self.lock.release(force=force)
