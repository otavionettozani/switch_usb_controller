class SwitchControllerType:
  LEFT_JOYCON=1
  RIGHT_JOYCON=2
  PRO_CONTROLLER=3

class SwitchController:
  def __init__(
    self,
    type,
    mac_address="64:b5:c6:40:e1:cc",
    initial_input="9100800092d87e0c987b00",
    color="323232ffffffffffffffffffff"
  ):
    self.mac_address = mac_address
    self.type = type
    self.initial_input = initial_input
    self.color = color

  def padding_message(self, message):
    return message + ("0" * (128-len(message)))

  def make_80_01_ans(self):
    address = self.mac_address.split(":")
    address.reverse()
    address_string = "".join(address)

    formatted_bytes = self.padding_message(f"8101000{self.type.value}{address_string}")
    return bytes.fromhex(formatted_bytes)

  def make_80_02_ans(self):
    formatted_bytes = self.padding_message("8102")
    return bytes.fromhex(formatted_bytes)

  