from enum import Enum

class SwitchControllerType(Enum):
  LEFT_JOYCON=1
  RIGHT_JOYCON=2
  PRO_CONTROLLER=3

class SwitchController:
  def __init__(
    self,
    type=SwitchControllerType.PRO_CONTROLLER,
    mac_address="64:b5:c6:40:e1:cc",
    initial_input="9100800092d87e0c987b00",
    color="323232ffffffffffffffffffff"
  ):
    self.mac_address = mac_address
    self.type = type
    self.initial_input = initial_input
    self.color = color

  def reverse_mac_address_hex(self):
    address = self.mac_address.split(":")
    address.reverse()
    address_string = "".join(address)
    return address_string
  
  def mac_address_hex(self):
    address = self.mac_address.split(":")
    address_string = "".join(address)
    return address_string
