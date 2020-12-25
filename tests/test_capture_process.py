#!/usr/bin/env python3

import sys
import time
import unittest

from async_output_capture import CaptureProcess


def stdout_printer(text, sleep):
    for i in range(50):
        sys.stdout.write('{}. {}\n'.format(i, text))
        if sleep:
            time.sleep(0.1)


def stderr_printer(text, sleep):
    for i in range(50):
        sys.stderr.write('{}. {}\n'.format(i, text))
        if sleep:
            time.sleep(0.1)


def get_all_output(process):
    output = ''
    while True:
        val = process.get_output()
        if val:
            output += val
        else:
            break
    return output


class TestStdOut(unittest.TestCase):
    def test_delayed_prints(self):
        p = CaptureProcess(target=stdout_printer, mode='stdout', args=('test', True))
        p.start()

        # Check during function execution
        curr_output = 0
        for _ in range(10):
            outputs = get_all_output(p)
            for output in outputs.splitlines():
                self.assertEqual(output, '{}. test'.format(curr_output))
                curr_output += 1
            time.sleep(0.2)

        p.join()
        # Check after function is done
        outputs = get_all_output(p)
        self.assertEqual(outputs.splitlines(), ['{}. test'.format(i) for i in range(curr_output, 50)])

    def test_instant_prints(self):
        p = CaptureProcess(target=stdout_printer, mode='stdout', args=('test', False))
        p.start()

        # Check during function execution
        curr_output = 0
        for _ in range(10):
            outputs = get_all_output(p)
            for output in outputs.splitlines():
                self.assertEqual(output, '{}. test'.format(curr_output))
                curr_output += 1
            time.sleep(0.2)

        p.join()
        # Check after function is done
        outputs = get_all_output(p)
        self.assertEqual(outputs.splitlines(), ['{}. test'.format(i) for i in range(curr_output, 50)])


class TestStdErr(unittest.TestCase):
    def test_delayed_prints(self):
        p = CaptureProcess(target=stderr_printer, mode='stderr', args=('test', True))
        p.start()

        # Check during function execution
        curr_output = 0
        for _ in range(10):
            outputs = get_all_output(p)
            for output in outputs.splitlines():
                self.assertEqual(output, '{}. test'.format(curr_output))
                curr_output += 1
            time.sleep(0.2)

        p.join()
        # Check after function is done
        outputs = get_all_output(p)
        self.assertEqual(outputs.splitlines(), ['{}. test'.format(i) for i in range(curr_output, 50)])

    def test_instant_prints(self):
        p = CaptureProcess(target=stderr_printer, mode='stderr', args=('test', False))
        p.start()

        # Check during function execution
        curr_output = 0
        for _ in range(10):
            outputs = get_all_output(p)
            for output in outputs.splitlines():
                self.assertEqual(output, '{}. test'.format(curr_output))
                curr_output += 1
            time.sleep(0.2)

        p.join()
        # Check after function is done
        outputs = get_all_output(p)
        self.assertEqual(outputs.splitlines(), ['{}. test'.format(i) for i in range(curr_output, 50)])


class TestIncorrectMode(unittest.TestCase):
    def test_incorrect_mode(self):
        with self.assertRaises(ValueError) as cm:
            CaptureProcess(target=stderr_printer, mode='non-existent-mode', args=('test'))


if __name__ == '__main__':
    unittest.main()
