"""Example of use of timed loops in an interactive, asynchronous environment."""


import random
from oclock import interactiveloop


@interactiveloop(interval=2)
def my_function():
    """Loop with function to be repeated at regular time intervals."""
    print('New Random Number: {:.3f}'.format(random.random()))


def main():
    """Run main_loop at the same time as the command line."""
    my_function()


if __name__ == '__main__':
    main()
