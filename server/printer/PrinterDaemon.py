from queue import Queue
from threading import Thread

from escpos.printer import Dummy, Usb

printer = Dummy()
# printer = Usb(0x0416, 0x5011, 4, 0x81, 0x03)
printer.set(density=2)


class PrinterDaemon(Thread):

    def __init__(self):
        super().__init__()
        self.print_queue = Queue()

    def run(self) -> None:
        while True:
            to_print = self.print_queue.get()
            printer._raw(to_print)
            if not self.print_queue.empty():
                input("Press enter to print next card. ")
