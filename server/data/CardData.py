from PIL import Image
from escpos.printer import Usb
from escpos.printer import Dummy


class CardData:

    IMAGE_WIDTH = 100

    def __init__(self):
        printer = Dummy()
        self.print_self(printer)
        self.raw_print = printer.output

    def get_card_image_uri(self) -> str:
        pass

    def print_self(self, printer, postfix="\n\n\n\n"):
        pass


if __name__ == "__main__":
    p = Usb(0x0416, 0x5011, in_ep=0x81, out_ep=0x3)
    hewwo = CardData("Dimun Light Longship", "7", "Machine, Dimun",
                     "On each turn end, deal 1 damage to the unit to "
                     "the right, then boost self by 2.", "Skellige",
                     "Bronze")
    p._raw(hewwo.raw_print)
