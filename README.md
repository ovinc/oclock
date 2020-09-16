# General information

**oclock** is a Python 3 module that provides a timing tools :

- The `Timer()` class allows for cancellable loops of constant duration.

- The `countdown()` function is a GUI countdown timer based on the Timer class.

- The `parse_time()` function returns a hours, min, sec tuple from a time string (e.g. `':2:25'`)

# Install

## Method 1

In a terminal:
```bash
pip install git+https://cameleon.univ-lyon1.fr/ovincent/oclock
```

## Method 2

- Clone the project or download directly the files into a folder.
- In a terminal, `cd` into the project or folder, where the __setup.py__ is, then
```bash
pip install .
```

# Quick start

## Loop timer

The most basic use of the `Timer()` class in Python code is
```python
from oclock import Timer
timer = Timer(interval=1)  # Loops will be of total duration 1 second
while condition:
    my_function()  # can be of any duration between 0 and 1 second
    timer.pause()
```
Note that if *my_function()* takes longer to execute than the required time interval, the Timer class does not try to compensate the extra time by making the next loop shorter. It just aims at making the total duration of the next loop be the requested interval again.

When the timer interacts with other threads in a concurrent environment, it can also be cancelled without having to wait for the end of the *timer.pause()* sleeping period. See details in the *Timer Class details* section below.

## Countdown GUI

To use the countdown GUI, there are two methods:

From a terminal:
```bash
python -m oclock 1:45:00   # start timer of duration 1 hour 45 minutes
python -m oclock 1:45:     # exactly the same as above
python -m oclock 00:02:00  # start 2-minute timer
python -m oclock :2:       # exactly the same as above
python -m oclock 00:00:05  # start 5-second timer
python -m oclock ::5       # exactly the same as above
```

From a python console:
```python
from oclock import countdown
countdown(1, 45)      # start timer of duration 1 hour 45 minutes
countdown(h=1, m=45)  # exactly the same as above
countdown(0, 2, 0)    # start 2-minute timer
countdown(m=2)        # exactly the same as above
countdown(0, 0, 5)    # start 5-second timer
countdown(s=5)        # exactly the same as above
```

When countdown is finished, 'Done' is displayed for 5 seconds in the GUI while the console displays *Countdown finished* and emits a sound 5 times in a row. Then the time passed since the end of countdown is displayed as a negative value in red. The program stops when the GUI window is closed.

## Parse time

The `parse_time()` function is used in the argument parsing of the countdown GUI from a terminal (see above). It transforms a string in the form `'h:m:s'` into a tuple `h, m, s`. Inputs of the form e.g. `'::5'` or `:2:`, `'3:30:'` are acceptable for 5 seconds, 2 minutes, and 3.5 hours, respectively.

# Timer Class details

## Methods

The methods associated with the timer class are the following:
```python
timer.change_interval(0.5)  # change interval to 0.5 s
timer.reset()  # starts counting time from here
timer.deactivate()  # immediate exiting of timer
timer.elapsed_time()  # Time in seconds since init or last reset
timer.elapsed_time(since_reset=False)  # Time in s since init
```
Note that all these changes take effect immediately, even if the timer is in a waiting phase, which can be useful if the loop is controlled by an external signal.

Also note that after deactivation, the `timer.pause()` command becomes equivalent to a `pass`, so that all following lines will be executed immediately and without any waiting time (i.e. as fast as possible if within a loop), until `timer.reset()` is called again.

Finally note that the `timer.change_interval()` call cancels any pause() that is in effect in order for the new interval to take effect immediatly, but does not reset the timer: in particular, `elapsed_time()` is not reset to zero.

## Attributes

The attributes associated with the timer class are the following:
```python
self.interval  # (float) value of the current interval in seconds
self.interval_exceeded  # (bool) True if the contents of the loop take longerto execute than the current requested interval
self.name  # optional name to give to the timer with timer=Timer(name='xyz')
self.warnings  # optional, if True, then there is a warning if the set time interval is too short compared to the execution time, set with Timer(warnings=True)
self.target  # (float) unix time of the target time for the next loop
self.stop_event  # (threading.Event object): is set when timer is deactivated
self.init_time   # Unix time at which the timer object has been intanciated
self.start_time  # Unix time since last reset (or init if no reset made)
```

## Example use

See *example.py* file of the module for such an example in an asynchronous environment; to run the example:
```bash
python -m oclock.example
```
in a terminal from the root of the module, or
```python
from oclock.example import main
main()
```
in a python console.

#### Accuracy test

See *test.py* file of the module for functions to test the accuracy of the timer. In particular:
```python
from oclock.test import test
test(dt=0.1, nloops=100, fmax=0.99)
```
tests the timing on 1000 loops of requested duration 0.1 second, using within the loop a function sleeping for a random amount of time between 0 and 0.99*dt.

Below are some quick preliminary results on timing accuracy in an Unix Environment (MacOS) and Windows, using `n=1000`, `fmax=0.99` for various values of `dt`.

###### Unix timing accuracy

|     Requested dt (s)    |   1    | 0.1  | 0.04  | 0.01 | 0.001 |
|:-----------------------:|:------:|:----:|:-----:|:----:|:-----:|
|Relative error in dt (%)*|< 0.0001|< 0.01| < 0.1 | 3.5  |  12   |
|Fluctuations in dt (ms)**|   0.6  | 0.5  |   1   |  1   |  0.2  |

###### Windows timing accuracy

|     Requested dt (s)    |   1   |  0.1  | 0.04 | 0.01 | 0.001 |
|:-----------------------:|:-----:|:-----:|:----:|:----:|:-----:|
|Relative error in dt (%)*|< 0.002|  0.9  | 6.1  |  62  |  833  |
|Fluctuations in dt (ms)**|  6.5  |  7.8  | 7.7  |  6.4 |  3.2  |

(*) measured by averaging all individual loop durations and comparing to the requested dt
(**) using one standard deviation


## Requirements

Python 3. To run some examples, Python : >= 3.6 is needed because of the use of f-strings.

## Author

Olivier Vincent
olivier.a-vincent@wanadoo.fr

## Contributors

Icon made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>