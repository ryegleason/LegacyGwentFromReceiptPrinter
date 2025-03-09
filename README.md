# LegacyGwentFromReceiptPrinter
Prints proxies for card games using a receipt printer.

I use a TEROW T5890K for printing (https://www.amazon.com/gp/product/B081SJTJ5G). Note that the python-escpos library used for printing is linux-exclusive, so your server must be a linux machine.

To start, run `nix develop`, then find your printer with `lsusb`. Fill out `.env` based on the instructions [here](https://python-escpos.readthedocs.io/en/latest/user/usage.html#usb-printer), e.g.
```
VENDOR_ID=0x0416
PRODUCT_ID=0x5011
IN_ENDPOINT=0x81
OUT_ENDPOINT=0x03
```

Next, check the permissions of your device. If lsusb shows `Bus XXX Device YYY`, then the file for your printer is `/dev/bus/usb/XXX/YYY/`. Add yourself to the group that owns it, or change the permissions for the device. Finally, run `python3 netcode.py` to start the server, and open <https://localhost:8080> to connect!
