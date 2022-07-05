#!/bin/bash

DIR="$(realpath $(dirname "${BASH_SOURCE[0]}"))"

cd /sys/kernel/config/usb_gadget/


mkdir -p procontroller
cd procontroller
echo 0x057e > idVendor
echo 0x2009 > idProduct
echo 0x0200 > bcdDevice
echo 0x0200 > bcdUSB
echo 0x00 > bDeviceClass
echo 0x00 > bDeviceSubClass
echo 0x00 > bDeviceProtocol

mkdir -p strings/0x409
echo "000000000001" > strings/0x409/serialnumber
echo "Nintendo Co., Ltd." > strings/0x409/manufacturer
echo "Pro Controller" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo "Nintendo Switch Pro Controller" > configs/c.1/strings/0x409/configuration
echo 500 > configs/c.1/MaxPower
echo 0xa0 > configs/c.1/bmAttributes

mkdir -p functions/hid.usb0
echo 0 > functions/hid.usb0/protocol
echo 0 > functions/hid.usb0/subclass
echo 64 > functions/hid.usb0/report_length
cat "$DIR/hid-descriptor" | xxd -r -ps > functions/hid.usb0/report_desc

ln -s functions/hid.usb0 configs/c.1/

ls /sys/class/udc > UDC
