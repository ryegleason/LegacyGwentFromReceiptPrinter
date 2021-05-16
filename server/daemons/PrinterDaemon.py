import time
from queue import Queue
from threading import Thread

from escpos.printer import Dummy, Usb

DRY_RUN = True

if DRY_RUN:
    printer = Dummy()
else:
    printer = Usb(0x0416, 0x5011, in_ep=0x81, out_ep=0x3)


class PrinterDaemon(Thread):

    def __init__(self):
        super().__init__()
        self.print_queue = Queue()

    def run(self) -> None:
        while True:
            to_print = self.print_queue.get()
            if not DRY_RUN:
                printer.open()
            printer._raw(to_print)
            if not DRY_RUN:
                printer.close()
            # time.sleep(2)
