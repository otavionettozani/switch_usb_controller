import os
import threading
import time
from .message import RequestMessage
from enum import Enum

class SocketState(Enum):
  Closed = 0
  Opening = 1
  Open = 2

class Socket:
  def __init__(self, message_callback, gadget_name = "procontroller", hid_file_location = "/dev/hidg0"):
    self.gadget_name = gadget_name
    self.hid_file_location = hid_file_location
    self.message_callback = message_callback
    self.state = SocketState.Closed
    self.timer = 0
    self.socket_thread = None
    self.timer_thread = None

  def open(self):
    self.state = SocketState.Opening
    os.system(f'echo > /sys/kernel/config/usb_gadget/{self.gadget_name}/UDC')
    os.system(f'ls /sys/class/udc > /sys/kernel/config/usb_gadget/{self.gadget_name}/UDC')
    time.sleep(0.5)
    self.data_file = os.open(self.hid_file_location, os.O_RDWR | os.O_NONBLOCK)
    self.socket_thread = threading.Thread(target=self._socket_thread)
    self.timer_thread = threading.Thread(target =self._timer_thread)

    self.socket_thread.start()
    self.timer_thread.start()
    self.state = SocketState.Open
  
  def send(self, data):
    os.write(self.data_file, data)

  def _socket_thread(self):
    while True:
      try:
        data = os.read(self.data_file, 128)
        if len(data) == 0:
          continue
        message = RequestMessage.parse(data)
        self.message_callback(message)
      except BlockingIOError:
        pass
      except ValueError, e:
        print("Message Error")
        print(str(e))
        pass
      except:
        print('unknown switch_output error')
        os.exit(1)

  def _timer_thread(self):
    while True:
      self.timer = (self.timer + 3) % 256
      time.sleep(0.03)
