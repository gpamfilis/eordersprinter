# e
# import sys
# sys.setdefaultencoding('utf8')
# https://askubuntu.com/questions/3299/how-to-run-cron-job-when-network-is-up
# https://stackoverflow.com/questions/11706215/how-to-fix-git-error-object-file-is-empty
# https://unix.stackexchange.com/questions/57852/crontab-job-start-1-min-after-reboot
import requests
import json
import time
from escpos.printer import Usb
from greeklish.converter import Converter
# from constants import *

from escpos.constants import CHARCODE_GREEK
# Adapt to your needs
# todo: Beep when new order comes in
def order_setup(order_id):
    myconverter = Converter(max_expansions=4)

    p = Usb(0x471, 0x55, 0, 0x82, 0x2)
    # p.codepa
    # p.device.write(p.out_ep, CHARCODE_GREEK, 5000)

    # p = Usb(0x1d6b, 0x2, 0, 0x82, 0x2)
    # p.codepage = 'cp1253'
    # p.charcode(code='AUTO')
    # p.device.read(p.in_ep, 1)

    res = requests.get('http://www.e-orders.org/api/app/order?order_id={0}'.format(order_id))
    res_json = json.loads(res.text)
    items = res_json['items']
    print(items)
    total_cost = 0
    p.set(align='center', text_type='B', width=3, height=3)
    p.text('DELTIO PARAGELIAS'+"\n")

    p.set(align='center', text_type='B', width=2, height=2)
    table_name = myconverter.convert(items['items'][0]['table_name'])[0]

    p.text(table_name+"\n")
    p.set(align='center', text_type='normal', width=1, height=1)
    p.text(items['datetime']+"\n")

    for item in items['items']:
        total_cost+=item['total_cost']
        item_name = myconverter.convert(item['name'])[0]

        p.set(align='left', text_type='B', width=2, height=1)
        # p.text(str(item['quantity'])+'X '+item['name']+'\n')
        p.text(str(item['quantity'])+'X '+item_name+'\n')
        comment = item['comments']


        p.set(align='center', text_type='normal', width=2, height=1)

        for content in item['contents']:
            if content['changed'] == 1:
                if content['default'] == 0:
                    content_name = myconverter.convert(content['content_name'])[0]

                    p.text('ME   '+content_name+'\n')

        p.set(align='right', text_type='normal', width=1, height=1)
        print(comment)
        if comment == '':
            pass
        else:
            comment_name = myconverter.convert(item['comments'])[0]

            # p.text('COMMENTS: '+item['comments'] + "\n")
            p.text('COMMENTS: ' + comment_name + "\n")
    p.set(align='center', text_type='B', width=3, height=3)
    p.text('\n')

    p.text('TOTAL: '+str(total_cost)+"\n")
    p.text('\n')
    p.cut()
    # RT_STATUS = DLE + EOT
    # RT_STATUS_ONLINE = RT_STATUS + b'\x01'
    # RT_STATUS_PAPER = RT_STATUS + b'\x04'
    # p.barcode()
    # method_list = [func for func in dir(p) if callable(getattr(p, func))]
    # print('device: ', p.query_status(PAPER_FULL_CUT))
    # print('device: ', p.query_status(PAPER_FULL_CUT))
    # e = "\x10\x04\x04"
    # p.device.write(p.out_ep, RT_STATUS_PAPER)
    # print('device: ', )
    # print('device: ', )
    # print('device: ', p._raw(RT_STATUS_ONLINE))
    # print('device: ', p._read())
    p.close()



def checkout_setup(checkout_id):
    p = Usb(0x471, 0x55, 0, 0x82, 0x02)
    myconverter = Converter(max_expansions=4)

    # p.device.read(p.in_ep, 1)

    res = requests.get('http://www.e-orders.org/api/printer/checkout-print?checkout_id={0}'.format(checkout_id))
    res_json = json.loads(res.text)
    print('response', res_json)
    items = res_json[0]
    print(items)

    p.set(align='center', text_type='B', width=3, height=3)
    p.text('CHECKOUT'+"\n")

    p.set(align='center', text_type='B', width=2, height=2)
    p.text(items['table_name']+"\n")
    p.set(align='center', text_type='normal', width=1, height=1)
    p.text(items['datetime']+"\n")

    for item in items['items']:
        p.set(align='left', text_type='B', width=2, height=1)
        p.text(str(item['quantity']) + 'x  '+ myconverter.convert(item['name'])[0]+'\n')
        p.set(align='right', text_type='B', width=1, height=1)
        p.text(str(item['quantity']) + ' x '+str(item['cost']) + '  sub total: ' + str(item['total_item_cost']) + '$' + '\n')
        # comment = item['comments']
    p.set(align='center', text_type='B', width=3, height=3)
    p.text('TOTAL: '+str(items['total'])+"\n")
    # p.text('\n\n\n\n\n\n\n\n\n\n\n\n')
    # p.text('\n\n\n\n\n\n\n\n\n\n\n\n')
    p.text('\n\n\n')
    # p.text('\n\n\n')
    p.cut()

    p.close()





def list_orders(store_id=1):
    print('list_orders')
    res = requests.get('http://www.e-orders.org/api/printer/orders-print?store_id={0}'.format(store_id))
    try:
        res_json = json.loads(res.text)
        print(res_json)
        return res_json['ids']
    except Exception as e:
        return None

def list_checkouts(store_id=1):
    print('list_checkouts')
    res = requests.get('http://www.e-orders.org/api/printer/checkout-print?store_id={0}'.format(store_id))
    res_json = json.loads(res.text)
    print(res_json)
    return res_json['ids']


# order_setup(orders[0])
try:

    with open('/home/pi/config.json') as f:
    # with open('/home/kasper/Desktop/config.json') as f:
        data = json.load(f)

    store_id = data['store_id']
    print('retrieving data for store id: ',store_id, type(store_id))

    while True:
        try:
            order_ids = list_orders(store_id=store_id)[:]
            # checkout_ids = list_checkouts()[:]
            print('orders: ', order_ids)
            # print('checkouts: ', checkout_ids)
            time.sleep(1)

            for order_id in order_ids:
                order_ids = list_orders(store_id=store_id)[:]
                # print(order_ids)
                print(order_id)
                time.sleep(1)
                try:
                    order_setup(order_id)
                    res_pos = requests.post('http://www.e-orders.org/api/printer/orders-print?order_id={0}'.format(order_id))
                    print('responce', res_pos)
                except Exception as e:
                    print(e)
                    print('deleting')
                    res_delete = requests.delete('http://www.e-orders.org/api/v1/mobile/printerorders?order_id={0}'.format(order_id))

            # for checkout_id in checkout_ids:
            #     checkout_ids = list_checkouts()[:]
            #     # print(order_ids)
            #     print(checkout_id)
            #     time.sleep(1)
            #     try:
            #         checkout_setup(checkout_id)
            #         res_pos = requests.post('http://www.e-orders.org/api/printer/checkout-print?checkout_id={0}'.format(checkout_id))
            #         print('responce', res_pos)
            #     except Exception as e:
            #         print(e)
        except Exception as e:
            print(e)

    # # p = Usb(0x471, 0x55, 0, 0x82, 0x2)
    # # p.device.write(p.out_ep, RT_STATUS_PAPER, 5000)
    # # p.device.read(p.in_ep, 256, 5000)
    # # p.close()
    #
    # import usb
    # # dev = None
    # # while dev is None:
    # dev = usb.core.find(idVendor=0x471, idProduct=0x55)
    # #
    # msg = 'text'
    # dev.write(0x2, RT_STATUS_PAPER, 10000)
    # ret = dev.read(0x82, len(RT_STATUS_PAPER), 5000)
    # sret = ''.join([chr(x) for x in ret])

except Exception as e:
    print(e)
