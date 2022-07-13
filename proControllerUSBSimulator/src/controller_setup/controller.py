from enum import Enum
from math import floor

class SwitchControllerType(Enum):
  LEFT_JOYCON=1
  RIGHT_JOYCON=2
  PRO_CONTROLLER=3

class SwitchControllerState:
  def __init__(self):
    self.connection = 9
    self.battery = 1

    self.ZR = False
    self.R = False
    self.SR_right = False
    self.SL_right = False
    self.A = False
    self.B = False
    self.X = False
    self.Y = False

    self.charge_grip = True
    self.capture = False
    self.home = False
    self.L3 = False
    self.R3 = False
    self.plus = False
    self.minus = False

    self.ZL = False
    self.L = False
    self.SL_left = False
    self.SR_left = False
    self.Left = False
    self.Right = False
    self.Up = False
    self.Down = False

    self.left_stick_x = 0
    self.left_stick_y = 0

    self.right_stick_x = 0
    self.right_stick_y = 0

  # Sticks positions will vary between -1 and 1 in this object and they vary between 0 and 4095 in the controllers, so we need to do that conversion
  def get_left_stick_position_hex(self):
    horizontal_position = floor(2047 + 2048*self.left_stick_x)
    vertical_position = floor(2047 + 2048*self.left_stick_y)
    return self.position_to_bytes(horizontal_position, vertical_position)


  def get_right_stick_position_hex(self):
    horizontal_position = floor(2047 + 2048*self.right_stick_x)
    vertical_position = floor(2047 + 2048*self.right_stick_y)
    return self.position_to_bytes(horizontal_position, vertical_position)
  
  def position_to_bytes(self, horizontal_position, vertical_position):
    lower_second_byte = horizontal_position >> 8
    first_byte = horizontal_position & 0xff
    higher_second_byte = (vertical_position & 0xf) << 4
    third_byte = vertical_position >> 4
    second_byte = lower_second_byte | higher_second_byte
    
    return (first_byte << 16) | (second_byte << 8) | third_byte

class SwitchController:
  def __init__(
    self,
    type=SwitchControllerType.PRO_CONTROLLER,
    mac_address="64:b5:c6:40:e1:cc",
    color="323232ffffffffffffffffffff",
    state=SwitchControllerState()
  ):
    self.mac_address = mac_address
    self.type = type
    self.color = color
    self.state = state

  def reverse_mac_address_hex(self):
    address = self.mac_address.split(":")
    address.reverse()
    address_string = "".join(address)
    return address_string
  
  def mac_address_hex(self):
    address = self.mac_address.split(":")
    address_string = "".join(address)
    return address_string

  def state_hex(self):
    hex_data = 0

    hex_data |= self.state.connection << 84
    hex_data |= self.state.battery << 80
    
    hex_data |= self.state.ZR << 79
    hex_data |= self.state.R << 78
    hex_data |= self.state.SR_right << 77
    hex_data |= self.state.SL_right << 76
    hex_data |= self.state.A << 75
    hex_data |= self.state.B << 74
    hex_data |= self.state.X << 73
    hex_data |= self.state.Y << 72
    
    hex_data |= self.state.charge_grip << 71
    hex_data |= self.state.capture << 69
    hex_data |= self.state.home << 68
    hex_data |= self.state.L3 << 67
    hex_data |= self.state.R3 << 66
    hex_data |= self.state.plus << 65
    hex_data |= self.state.minus << 64

    hex_data |= self.state.ZL << 63
    hex_data |= self.state.L << 62
    hex_data |= self.state.SL_left << 61
    hex_data |= self.state.SR_left << 60
    hex_data |= self.state.Left << 59
    hex_data |= self.state.Right << 58
    hex_data |= self.state.Up << 57
    hex_data |= self.state.Down << 56

    hex_data |= self.state.get_left_stick_position_hex() << 32
    hex_data |= self.state.get_right_stick_position_hex() << 8

    return f"{hex_data:x}"