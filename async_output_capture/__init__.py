#!/usr/bin/env python3
"""
async_output_capture
====================

Author: Mátyás Schubert

Description: async_output_capture is a library of classes
             which can be used to run functions asynchronously
             while capturing their output written to stdout and
             stderr in real time.
"""
from .async_output_capture import StderrCaptureProcess, StdoutCaptureProcess

__version__ = '0.1.1'
