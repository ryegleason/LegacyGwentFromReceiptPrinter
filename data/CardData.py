from escpos.printer import Dummy


class CardData:

    def __init__(self):
        printer = Dummy()
        # self.name = "default"
        self.print_self(printer)
        self.raw_print = printer.output

    def queue_print(self, print_queue):
        print_queue.put(self.raw_print)

    def get_card_image_uri(self) -> str:
        pass

    def print_self(self, printer, postfix="\n\n\n\n"):
        pass

