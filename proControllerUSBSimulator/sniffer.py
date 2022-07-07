import os
import threading
import time


os.system('echo > /sys/kernel/config/usb_gadget/procontroller/UDC')
os.system('ls /sys/class/udc > /sys/kernel/config/usb_gadget/procontroller/UDC')

time.sleep(0.5)

simulated = os.open('/dev/hidg0', os.O_RDWR | os.O_NONBLOCK)
real = os.open('/dev/hidraw0', os.O_RDWR | os.O_NONBLOCK)


def switch_output():
  while True:
    try:
      input_data = os.read(simulated, 128)
      print('>>>', input_data.hex())
      os.write(real, input_data)
    except BlockingIOError:
      pass
    except:
      print('unknown switch_output error')
      os.exit(1)


def switch_input():
  while True:
    try:
      output_data = os.read(real, 128)
      print('<<<', output_data.hex())
      os.write(simulated, output_data)
    except BlockingIOError:
      pass
    except:
      print('unknown switch_input error')
      os._exit(1)

threading.Thread(target=switch_output).start()
threading.Thread(target=switch_input).start()


