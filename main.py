from mangle import *
import urwid

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

LOGO = """
  _       _       _                 _           _
 | |_ ._.| |._.  | |_ ___ _ _ _ __ (_)_ _  __ _| |
 |  _/ _ \ / _ \ |  _/ -_) '_| '  \| | ' \/ _` | |
  \__\___/_\___/  \__\___|_| |_|_|_|_|_||_\__,_|_|"""

PALETTE = [
    ('header', 'white', 'black'),
    ('normal', 'white', 'black'),
    ('focus', 'black', 'dark cyan', 'standout'),
    ('negative', 'light red', 'black'),
    ('positive', 'light green', 'black'),
    ('bold', 'white, bold', 'black')
]

urwid.set_encoding("UTF-8")

class SelectableText(urwid.Edit):
    def valid_char(self, ch):
        return False

def lc(data):
    body = []
    for d in reversed(data):
        columns = [SelectableText(str(v)) for v in d]

        body.append(
            urwid.AttrMap(
                urwid.Columns(columns),
                'normal', 'focus'
            )
        )

    return body

cols, data = get_data()
listing = urwid.SimpleFocusListWalker(lc(data))

class ScriptChangeHandler(PatternMatchingEventHandler):
    patterns = ['calc.py']

    def dispatch(self, event):
        from random import randint
        cols, data = get_data()
        listing[:] = lc(data)
        mainloop.draw_screen()

def unhandled_input(keys):
    if keys=='q': raise urwid.ExitMainLoop()

header = urwid.AttrMap(urwid.Columns(
    [
        urwid.Text(u'X')
    ]
), 'bold')

main = urwid.Frame(
    urwid.ListBox(listing),
    header=urwid.Pile([
        header,
        urwid.BoxAdapter(urwid.SolidFill(u"\u2500"), 1)
    ])
)

event_handler = ScriptChangeHandler()
observer = Observer()
observer.schedule(event_handler, '.')
observer.start()

mainloop = urwid.MainLoop(
    main,
    palette=PALETTE,
    unhandled_input=unhandled_input
)
mainloop.run()
