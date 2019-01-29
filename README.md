# terminal_size

## What?
terminal_size is a small Python snippet that aims to detect any terminal emulator size on any platform (Windows, Mac, Linux, tput, CYGWIN, your toaster, etc.). If successful, its main function **get_terminal_size()** returns a tuple composed by two values, representing respectively the width and the height of the terminal emulator in which your code is running.

## How?
Usage:

```
from terminal_size import get_terminal_size
term_size = get_terminal_size()
```

The types returned to term_size in the usage case above can be **tuple** (if size was successfully detected) or **None** (in case the code could not detect the dimensions successfully).
You can test its return with:

```
isinstance(term_size, tuple) and len(term_size) == 2
```

Any other weird stuff that may happen during the detection attempt will simply break and raise.
