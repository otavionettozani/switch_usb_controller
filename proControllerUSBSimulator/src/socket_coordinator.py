from usb_socket.socket import Socket
from usb_socket.message import ResponseFactory, MessageCommand, SetupMessageSubcommand
import threading
import time

class SocketCoordinator:
  def __init__(self, controller):
    self.socket = Socket(self.handle_message)
    self.responseFactory = ResponseFactory(controller)

  def start(self):
    self.socket.open()


  def handle_message(self, message):
    print("<<<")
    print(message.__dict__)
    if message.command == MessageCommand.Setup and message.subcommand == SetupMessageSubcommand.ActivateUsb:
      self.input_thread = threading.Thread(target=self._input_thread)
      self.input_thread.start()
    else:
      response = self.responseFactory.response_for_request(message, self.socket.timer)
      print(">>>")
      print(response)
      if response:
        self.socket.send(response)
  

  def _input_thread(self):
    print("input thread")
    while True:
      response = self.responseFactory.response_for_controller(self.socket.timer)
      self.socket.send(response)
      time.sleep(0.03)
