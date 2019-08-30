from escpos.printer import Usb


# Adapt to your needs
p = Usb(0x471, 0x55, 0, 0x82, 0x2)

p.text("Hello World\n")
# Print image
# p.image("logo.gif")
# Print QR Code
p.qr("You can readme from your smartphone")
# Print barcode
p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
# Cut paper
# p.cut()
p.text('test')
p.text('test')
p.barcode('123456', 'CODE39')
p.cut()
# import usb.core
# import usb.util
#
# # find our device
# dev = usb.core.find(0x471, 0x55)
#
# # was it found?
# if dev is None:
#     raise ValueError('Device not found')
#
# # set the active configuration. With no arguments, the first
# # configuration will be the active one
# # dev.set_configuration()
# #
# # # get an endpoint instance
# # cfg = dev.get_active_configuration()
# # intf = cfg[(0,0)]
# #
# # ep = usb.util.find_descriptor(
# #     intf,
# #     # match the first OUT endpoint
# #     custom_match = \
# #     lambda e: \
# #         usb.util.endpoint_direction(e.bEn dpointAddress) == \
# #         usb.util.ENDPOINT_OUT)
# #
# # assert ep is not None
# #
# # # write the data
# # ep.write('test')