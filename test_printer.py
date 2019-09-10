import requests
import json
import time
from escpos.printer import Usb

from constants import *

p = Usb(0x471, 0x55, 0, 0x82, 0x2)
# p = Usb(0x1d6b, 0x2, 0, 0x82, 0x2)


p.set(align='center', text_type='B', width=3, height=3)
p.text('NEW ORDER'+"\n")

p.text('\n\n\n\n\n\n\n\n\n\n\n\n')
p.cut()

p.close()

if __name__ == '__main__':
    pass
