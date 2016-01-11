import os
import subprocess
import time

def set_clipboard(num, val):
    proc = subprocess.Popen(
        ['xsel', '--display', ':' + num, '-b', '-i'],
        stdin=subprocess.PIPE,
    )
    proc.communicate(input=val)
    proc.wait()

def get_clipboard(num):
    return subprocess.check_output(
        ['xsel', '--display', ':' + num, '-b', '-o'],
    )

def get_displays():
    displays = set()
    for name in os.listdir('/tmp/.X11-unix'):
        displays.add(name[1:])
    return displays

def set_clipboards(source, val, displays):
    for display in displays:
        if display == source:
            continue
        set_clipboard(display, val)

clipboard = None
clipboards = {}
cur_displays = set()
while True:
    displays = get_displays()

    for display in cur_displays - displays:
        cur_displays.remove(display)
        clipboards.pop(display)

    cur_displays = displays

    for display in displays:
        val = get_clipboard(display)
        if display in clipboards:
            if val != clipboards[display] and val != clipboard:
                clipboards[display] = val
                clipboard = val
                set_clipboards(display, val, displays)
        else:
            clipboards[display] = val

    time.sleep(0.1)
