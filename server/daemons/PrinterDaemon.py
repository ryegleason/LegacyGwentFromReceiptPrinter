import os
from queue import Queue
from threading import Thread

from dotenv import load_dotenv
from escpos.printer import Dummy, Usb
import escpos.constants

load_dotenv()
DRY_RUN = False

if DRY_RUN:
    printer = Dummy()
else:
    printer = Usb(int(os.getenv("VENDOR_ID"), base=16),
                  int(os.getenv("PRODUCT_ID"), base=16),
                  in_ep=int(os.getenv("IN_ENDPOINT"), base=16),
                  out_ep=int(os.getenv("OUT_ENDPOINT"), base=16))


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
