from PIL import Image
from escpos.printer import Usb
from escpos.printer import Dummy

from data.CardData import CardData


class SimpleCardData(CardData):

    IMAGE_WIDTH = 100

    def __init__(self, name, top_right, typeline, body, bottom_left, bottom_right, artwork):
        self.name = name
        self.top_right = top_right
        self.typeline = typeline
        self.body = body
        self.botttom_left = bottom_left
        self.bottom_right = bottom_right
        self.artwork = artwork
        super().__init__()

    def get_card_image_uri(self) -> str:
        pass

    def print_self(self, printer, postfix="\n\n\n"):
        printer.set(align="left")
        printer.text(self.name + "\n")
        printer.set(align="right")
        printer.text(self.top_right + "\n")
        #if self.artwork is not None:
        #    printer.set(align="center")
        #    printer.image(img_source=self.artwork, impl="bitImageRaster")
        printer.text("\n")
        printer.set(align="left")
        printer.text("\n")
        printer.text(self.typeline + "\n\n")
        printer.text(self.body + "\n\n")
        printer.text(self.botttom_left + "\n")
        printer.set(align="right")
        printer.text(self.bottom_right + postfix)
