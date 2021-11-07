from tkinter import *
import difflib as dl
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
import tkinter.font as tkfont

import threading

from client import Client


class Editor:
    def __init__(self, file):
        self.file = file
        self.root = Tk()
        self.root.geometry("350x250")
        self.root.title("Chicken nugget")
        self.root.minsize(height=250, width=300)

        self.text = Text(self.root, wrap=WORD, font=("Arial", 12))
        self.text.pack(fill=BOTH)
        self.set(self.file.read())

        self.contents = self.text.get("1.0", END)

        self.root.bind('<Control-s>', self.save)

        cdg = ic.ColorDelegator()
        cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
        cdg.idprog = re.compile(r'\s+(\w+)', re.S)

        font = tkfont.Font(font=self.text['font'])

        # Set Tab size
        tab_size = font.measure('  ')
        self.text.config(tabs=tab_size)

        cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': '#FFFFFF'}

        # These five lines are optional. If omitted, default colours are used.
        cdg.tagdefs['COMMENT'] = {'foreground': '#666', 'background': '#FFFFFF'}
        cdg.tagdefs['KEYWORD'] = {'foreground': '#9B3B6A', 'background': '#FFFFFF'}
        cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#FFFFFF'}
        cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': '#FFFFFF'}
        cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#FFFFFF'}

        ip.Percolator(self.text).insertfilter(cdg)

        self.root.bind('<KeyRelease>', self.update)

        self.client = Client("127.0.0.1", 12345, self)

        self.root.mainloop()

    def save(self, event):
        inp = self.text.get("1.0", END)
        self.file.save(inp)

    def update(self, event):
        new = self.text.get("1.0", END)
        for i, s in enumerate(dl.ndiff(self.contents, new)):
            if s[0] == ' ':
                continue
            elif s[0] == '-':
                print(u'Delete "{}" from position {}({})'.format(s[-1], i, self.line_index(i, self.contents)))
            elif s[0] == '+':
                self.client.send("new|" + self.line_index(i, self.contents) + "|" + s[-1])

        self.contents = new

    def set(self, contents):
        self.text.insert("1.0", contents)

    def insert(self, index, contents):
        self.text.insert(index, contents)

    def line_index(self, index, string):
        char_total = 0
        line_num = 1
        i_str = ""
        for line in string.split("\n"):
            if index <= char_total + len(line) + 1:
                break
            else:
                line_num += 1
                char_total += len(line) + 1
        return str(line_num) + "." + str((index - char_total))

