## General information

**oclock** is a Python 3 module that provides a timer. Its purpose is to provide loops of constant duration no matter what the execution time of the contents of the loop is, and with a possibility to exit the loop at any time including during the waiting period (timer is cancellable).

## Install

#### Method 1

In a terminal:
```bash
pip install git+https://cameleon.univ-lyon1.fr/ovincent/oclock
```

#### Method 2

- Clone the project or download directly the files into a folder.
- In a terminal, `cd` into the project or folder, where the __setup.py__ is, then
```bash
pip install .
```

## Quick start

The most basic use of the module is
```python
from oclock import Timer
timer = Timer(interval=1)  # Loops will be of total duration 1 second
while condition:
    my_function()  # One assumes here that my_func can set condition to False
    if not condition:
        break
    timer.pause()  # This is where the timer adapts the waiting time
```

#### Methods

The methods associated with the timer class are the following:
```python
timer.change_interval(0.5)  # change interval to 0.5 s
timer.reset()  # starts counting time from here
timer.deactivate()  # immediate exiting of timer
```
Note that all these changes take effect immediately, even if the timer is in a waiting phase, which can be useful if the loop is controlled by an external signal (see *\__main.py\__* file of the module for such an example in an asynchronous environment; to run the example, `python -m oclock`).

Also note that after deactivation, the `timer.pause()` command becomes equivalent to a `pass`, so that all following lines will be executed immediately.

#### Attributes
The attributes associated with the timer class are the following:
```python
timer.interval  # (float) value of the current interval in seconds
self.interval_exceeded  # (bool) True if the contents of the loop take longerto execute than the current requested interval
self.name  # optional name to give to the timer with timer=Timer(name='xyz')
self.warnings  # optional, if True, then there is a warning if the set time interval is too short compared to the execution time, set with Timer(warnings=True)
self.target  # (float) unix time of the target time for the next loop
timer.stop_event  # (threading.Event object): is set when timer is deactivated
```



## Requirements

Python 3. To run some examples, Python : >= 3.6 is needed because of the use of f-strings.

## Author

Olivier Vincent
olivier.a-vincent@wanadoo.fr