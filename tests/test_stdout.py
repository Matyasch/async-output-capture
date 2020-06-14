#!/usr/bin/env python3

import sys
from time import sleep

from async_output_capture import StdoutCaptureProcess


def sleepy_printer(text):
    for i in range(50):
        sys.stdout.write('{}. {}\n'.format(i, text))
        sleep(0.1)


def test_wait_sleepy_print_to_finish_and_check_after():
    p = StdoutCaptureProcess(target=sleepy_printer, args=('test',))
    p.start()
    p.join()

    # Check after function is done
    outputs = ''
    while True:
        val = p.get_output()
        if val:
            outputs += val
        else:
            break

    assert outputs.splitlines() == ['{}. test'.format(i) for i in range(50)]


def test_wait_sleepy_print_to_finish_and_check_during_and_after():
    p = StdoutCaptureProcess(target=sleepy_printer, args=('test',))
    p.start()

    # Check during function execution
    curr_output = 0
    for _ in range(10):
        outputs = ''
        while True:
            val = p.get_output()
            if val:
                outputs += val
            else:
                break
        for output in outputs.splitlines():
            assert output == '{}. test'.format(curr_output)
            curr_output += 1
        sleep(0.2)

    p.join()
    # Check after function is done
    outputs = ''
    while True:
        val = p.get_output()
        if val:
            outputs += val
        else:
            break

    assert outputs.splitlines() == ['{}. test'.format(i) for i in range(curr_output, 50)]


def instant_printer(text):
    for i in range(2000):
        sys.stdout.write('{}. {}\n'.format(i, text))


def test_wait_instant_print_to_finish_and_check_after():
    p = StdoutCaptureProcess(target=instant_printer, args=('test',))
    p.start()
    p.join()

    # Check after function is done
    outputs = ''
    while True:
        val = p.get_output()
        if val:
            outputs += val
        else:
            break

    assert outputs.splitlines() == ['{}. test'.format(i) for i in range(2000)]


def test_wait_instant_print_to_finish_and_check_during_and_after():
    p = StdoutCaptureProcess(target=instant_printer, args=('test',))
    p.start()

    # Check during function execution
    curr_output = 0
    for _ in range(10):
        outputs = ''
        while True:
            val = p.get_output()
            if val:
                outputs += val
            else:
                break
        for output in outputs.splitlines():
            assert output == '{}. test'.format(curr_output)
            curr_output += 1
        sleep(0.2)

    p.join()
    # Check after function is done
    outputs = ''
    while True:
        val = p.get_output()
        if val:
            outputs += val
        else:
            break

    assert outputs.splitlines() == ['{}. test'.format(i) for i in range(curr_output, 2000)]
