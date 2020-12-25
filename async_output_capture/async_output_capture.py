#!/usr/bin/env python3

import contextlib
import multiprocessing
from multiprocessing.queues import Queue
from queue import Empty


class CaptureProcess(multiprocessing.Process):
    def __init__(self, target=None, mode='stdout', args=(), kwargs={}):
        '''
        Specialized process module to capture standard output or standard error from functions:
            target  - Function to run asynchronously and capture output from
            mode    - Sets whether to capture standard output (stdout) or standard error (stderr)
            args    - Tuple for the target invocation
            kwargs  - Dictionary of keyword arguments for the target invocation
        '''
        super().__init__(target=target, args=args, kwargs=kwargs)

        if mode == 'stdout':
            self.redirect = contextlib.redirect_stdout
        elif mode == 'stderr':
            self.redirect = contextlib.redirect_stderr
        else:
            raise ValueError('Expected mode to be stdout or stderr instead of {}'.format(mode))

        self._queue = Queue(ctx=multiprocessing.get_context())
        setattr(self._queue, 'write', self._queue.put)

    def run(self):
        with self.redirect(self._queue):
            super().run()

    def get_output(self):
        try:
            return self._queue.get_nowait()
        except Empty:
            return None
