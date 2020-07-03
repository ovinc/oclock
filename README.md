## General information

This Python 3 module provides a cancellable timer. Its purpose is to provide loops of constant duration no matter what the execution time of the contents of the loop is, and with a possibility to exit the loop at any time including during the waiting period.

## Install

For now the package is not listed in PyPI, so one needs to do a manual install.
Follow the steps below:

- Clone the project or download directly the files into a folder.
- In the command line, `cd` into the project or folder, where the __setup.py__ is.
- run `python -m pip install .`

Now, the package can be imported in Python with `import oclock`.

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

The methods associated with the timer class are the following:
```python
timer.change_interval(0.5)  # change interval to 0.5 s
timer.reset()  # starts counting time from here
timer.deactivate()  # immediate exiting of timer
```
Note that all these changes take effect immediately, even if the timer is in a waiting phase, which can be useful if the loop is controlled by an external signal (see *\__main.py\__* file of the module for such an example in an asynchronous environment; to run the example, `python -m oclock`).

Also note that after deactivation, the `timer.pause()` command becomes equivalent to a `pass`, so that all following lines will be executed immediately.


## Requirements

Python 3. To run some examples, Python : >= 3.6 is needed because of the use of f-strings.

## Author

Olivier Vincent
olivier.a-vincent@wanadoo.fr