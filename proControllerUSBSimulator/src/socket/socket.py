import os
import threading
import time
from message import Message

class Socket:
  def __init__(self, message_callback, gadget_name = "procontroller", hid_file_location = "/dev/hidg0"):
    self.gadget_name = gadget_name
    self.hid_file_location = hid_file_location
    self.message_callback = message_callback

  def open(self):
    os.system(f'echo > /sys/kernel/config/usb_gadget/{self.gadget_name}/UDC')
    os.system(f'ls /sys/class/udc > /sys/kernel/config/usb_gadget/{self.gadget_name}/UDC')
    self.data_file = os.open(self.hid_file_location, os.O_RDWR | os.O_NONBLOCK)
    threading.Thread(target=_socket_thread).start()

  def _socket_thread(self):
    while True:
      try:
        data = os.read(self.data_file, 128)
        message = Message.parse(data)
        self.message_callback(message)
      except BlockingIOError:
        pass
      except:
        print('unknown switch_output error')
        os.exit(1)

