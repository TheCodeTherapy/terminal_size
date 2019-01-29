def get_terminal_size():
    try:
        from platform import system
        operating_system = system()
        xy = None
        if operating_system == 'Windows':
            xy = get_terminal_size_windows()
            if xy is None:
                xy = get_terminal_size_tput() # needed for window's python in cygwin's xterm
        if operating_system in ['Linux', 'Darwin'] or operating_system.startswith('CYGWIN'):
            xy = get_terminal_size_linux()
        return xy
    except:
        raise


def get_terminal_size_windows():
    try:
        from struct import unpack
        from ctypes import windll, create_string_buffer
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy) = unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass
    return None


def get_terminal_size_tput():
    try:
        from subprocess import check_call
        from shlex import split as shsplit
        x = int(check_call(shsplit('tput cols')))
        y = int(check_call(shsplit('tput lines')))
        return (x, y)
    except:
        pass
    return None


def get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            from fcntl import ioctl
            from termios import TIOCGWINSZ
            from struct import unpack
            import os
            cr = unpack('hh', ioctl(fd, TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])


if __name__ == "__main__":
    try:
        term_size = get_terminal_size()
        if term_size is not None and isinstance(term_size, tuple):
            if len(term_size) == 2:
                size = "{0}x{1}".format(term_size[0], term_size[1])
                print("{0} {1}".format("Terminal Size:", size))
            else:
                print("ERROR: Unable to detect terminal size properly.")
        else:
            print("ERROR: Unable to detect terminal size.")
    except:
        raise
