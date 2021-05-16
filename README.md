# LegacyGwentFromReceiptPrinter
Prints proxies for card games using a recipt printer.

I use a TEROW T5890K for printing (https://www.amazon.com/gp/product/B081SJTJ5G). Note that the python-escpos library used for printing is linux-exclusive, so your server must be a linux machine.

To use, install the app in "client" onto each players' phone, then connect the printer to your server computer and run main.py in the server directory. The IP to enter on the app is the server's IP.
