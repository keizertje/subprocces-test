import os
from subprocess import *
import threading


class Executor:
    def __init__(self, write_fn):
        self.process: Popen | None = None
        self.input_thread = None
        self.write_fn = write_fn

    def read_stdout(self):
        os.set_blocking(self.process.stdout.fileno(), False) # make read a non-blocking call
        while self.process.poll() is None:
            char = self.process.stdout.read()
            if char:
                self.write_fn(char)
        self.process.stdout.close()
        print("ended reading")

    def read_stderr(self):
        os.set_blocking(self.process.stderr.fileno(), False) # make read a non-blocking call
        while self.process.poll() is None:
            char = self.process.stderr.read()
            if char:
                self.write_fn(char, {"foreground": "red"})
        self.process.stderr.close()
        print("ended reading")

    def write_exitcode(self):
        self.write_fn(f"Process finished with exit code {self.process.wait()}\n", {"foreground": "blue"})

    def write_stdin(self, __s):
        self.process.stdin.write(__s.encode())
        self.process.stdin.flush()

    @property
    def is_running(self):
        print(f"self.process = {self.process}")
        return self.process.poll() is None

    def start(self, cmd):
        self.process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        threading.Thread(target=self.read_stdout, daemon=True).start()
        threading.Thread(target=self.read_stderr, daemon=True).start()
        threading.Thread(target=self.write_exitcode, daemon=True).start()
