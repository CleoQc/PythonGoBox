##########################
class KeyPoller():
    def __enter__(self):
        debug ("enter fct")
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        return self

    def __exit__(self, type, value, traceback):
        debug ("exit fct")
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def poll(self):
        """
           non-blocking method to get one character input from keyb
        """
        dr,dw,de = select.select([sys.stdin], [], [], 0)
        if not dr == []:
            return sys.stdin.read(1)
        return None

    def readKey(self):
        """
           blocking method to get one character input from keyb
        """
        debug ("readKey fct")
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ord(ch) == 3 or ord(ch) == 0x1b: # detect CtrlC or ESC
            raise KeyboardInterrupt
        return ch