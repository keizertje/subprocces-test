from tkinter import *
from executor import Executor


class App(Tk):
    tag_count = 0

    def __init__(self):
        super().__init__()

        self.executor = Executor(self.write)

        self.output = Text(self)
        self.input = Entry(self)
        self.startbtn = Button(text="start", command=lambda: self.start())

        self.startbtn.pack()
        self.output.pack(expand=True, fill=BOTH)
        self.input.pack(fill=X)

        self.input.bind("<Return>", lambda a: [self.handle_input(), self.after(10, lambda: self.input.focus())])

    def handle_input(self):
        print("handling input...")
        text = self.input.get()
        self.input.delete(0, END)

        if self.executor.is_running:
            print("sending input...")
            self.executor.write_stdin(text + "\n")

            self.write(text + "\n")

    def write(self, __s, style=None):
        self.output.insert(END, __s)

        if style is not None:
            print(str(self.tag_count), f"end-{len(__s)+1}c", "end-1c", sep="\t")
            self.output.tag_add(str(self.tag_count), f"end-{len(__s)+1}c", "end-1c")
            self.output.tag_configure(str(self.tag_count), **style)
            self.tag_count += 1

    def start(self):
        self.executor.start("python interactive_program.py")
