# Async Output Capture
A Specialized Process module for capturing standard and error output from functions ran asynchronously, in real time

## Example usage
Capture standard output of a function
```python
import sys
import time

from async_output_capture import CaptureProcess

def printer(text):
    for i in range(3):
        sys.stdout.write('{} {}'.format(text, i))
        time.sleep(0.1)

p = CaptureProcess(target=printer, mode='stdout', args=('hello',))
p.start()               # Start running printer function and capture its stdout

print(p.get_output())   # None
time.sleep(0.05)
print(p.get_output())   # hello 0
print(p.get_output())   # None
p.join()
print(p.get_output())   # hello 1
print(p.get_output())   # hello 2
```
The results printed are
```
None
hello 0
None
hello 1
hello 2
```
