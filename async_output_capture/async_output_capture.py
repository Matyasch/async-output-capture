#!/usr/bin/env python3

import contextlib
import multiprocessing
from multiprocessing.queues import Queue
from queue import Empty


class WritableQueue(Queue):
    def write(self, s):
        self.put(s)


class StdoutCaptureProcess(multiprocessing.Process):
    def __init__(self, target=None, name=None, args=(), kwargs={}):
        super().__init__(target=target, name=name, args=args, kwargs=kwargs)
        self._queue = WritableQueue(ctx=multiprocessing.get_context())

    def run(self):
        with contextlib.redirect_stdout(self._queue):
            super().run()

    def get_output(self):
        try:
            return self._queue.get_nowait()
        except Empty:
            return None


class StderrCaptureProcess(multiprocessing.Process):
    def __init__(self, target=None, name=None, args=(), kwargs={}):
        super().__init__(target=target, name=name, args=args, kwargs=kwargs)
        self._queue = WritableQueue(ctx=multiprocessing.get_context())

    def run(self):
        with contextlib.redirect_stderr(self._queue):
            super().run()

    def get_output(self):
        try:
            return self._queue.get_nowait()
        except Empty:
            return None
