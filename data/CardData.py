from escpos.printer import Dummy

class CardData:

    def __init__(self):
        printer = Dummy()
        printer.profile.profile_data["media"]["width"]["pixels"] = 50000 # dummy value to suppress warnings
        self.print_self(printer)
        self.raw_print = printer.output

    def queue_print(self, print_queue):
        print_queue.put(self.raw_print)

    def get_card_image_uri(self) -> str:
        pass

    def print_self(self, printer, postfix="\n\n\n\n"):
        pass

