#!/usr/bin/env python3

import contextlib
import multiprocessing
from multiprocessing.queues import Queue
from queue import Empty


class _BaseCaptureProcess(multiprocessing.Process):
    def __init__(self, target=None, name=None, args=(), kwargs={}):
        super().__init__(target=target, name=name, args=args, kwargs=kwargs)
        self._queue = Queue(ctx=multiprocessing.get_context())
        setattr(self._queue, 'write', self._queue.put)

    def get_output(self):
        try:
            return self._queue.get_nowait()
        except Empty:
            return None


class StdoutCaptureProcess(_BaseCaptureProcess):
    def __init__(self, target=None, name=None, args=(), kwargs={}):
        super().__init__(target=target, name=name, args=args, kwargs=kwargs)

    def run(self):
        with contextlib.redirect_stdout(self._queue):
            super().run()


class StderrCaptureProcess(_BaseCaptureProcess):
    def __init__(self, target=None, name=None, args=(), kwargs={}):
        super().__init__(target=target, name=name, args=args, kwargs=kwargs)

    def run(self):
        with contextlib.redirect_stderr(self._queue):
            super().run()
