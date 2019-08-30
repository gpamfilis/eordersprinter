#!/usr/bin/python
import sys
import usb.core
# find USB devices
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
    # print(cfg)
    # sys.stdout.write('Decimal VendorID=' + str(cfg) + '\n')
    # sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
    sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')
    # sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.bcdDevice) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')


import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x471, idProduct=0x55)

# was it found?
if dev is None:
    raise ValueError('Device not found')

print(dev)
# set the active configuration. With no arguments, the first
# configuration will be the active one
# dev.set_configuration()
#
# # get an endpoint instance
# cfg = dev.get_active_configuration()
# intf = cfg[(0,0)]
#
# ep = usb.util.find_descriptor(
#     intf,
#     # match the first OUT endpoint
#     custom_match = \
#     lambda e: \
#         usb.util.endpoint_direction(e.bEndpointAddress) == \
#         usb.util.ENDPOINT_OUT)
#
# assert ep is not None
#
# # write the data
# ep.write('test')