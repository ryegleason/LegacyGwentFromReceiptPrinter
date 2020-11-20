from escpos.printer import Usb
from escpos.printer import Dummy


class Card:

    def __init__(self, name, top_right, image, typeline, body, bottom_left, bottom_right):
        self.name = name
        self.top_right = top_right
        self.image = image
        self.typeline = typeline
        self.body = body
        self.botttom_left = bottom_left
        self.bottom_right = bottom_right

    def print_self(self, printer):
        printer.set(align="left")
        printer.text(self.name + "\n")
        printer.set(align="right")
        printer.text(self.top_right + "\n")
        printer.set(align="center")
        printer.image(img_source=self.image, impl="bitImageRaster")
        printer.set(align="left")
        printer.text("\n")
        printer.text(self.typeline + "\n\n")
        printer.text(self.body + "\n\n")
        printer.text(self.botttom_left + "\n")
        printer.set(align="right")
        printer.text(self.bottom_right + "\n\n\n\n")


if __name__ == "__main__":
    d = Dummy()
    p = Usb(0x0416, 0x5011, in_ep=0x81, out_ep=0x3)
    hewwo = Card("Dimun Light Longship", "7", "dimun.jpg", "Machine, Dimun", "On each turn end, deal 1 damage to the unit to"
                                                                      " the right, then boost self by 2.", "Skellige", "Bronze")
    hewwo.print_self(d)
    p._raw(d.output)
