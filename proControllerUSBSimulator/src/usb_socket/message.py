from enum import Enum

class MessageCommand(Enum):
  Setup = 0x80
  UART = 0x01

class SetupMessageSubcommand(Enum):
  MacAddrRequest = 0x01
  Handshake = 0x02
  ActivateUsb = 0x04
  DeactivateUsb = 0x05

class UARTMessageSubcommand(Enum):
  BluetoothPairing = 0x01
  DeviceInfo = 0x02
  InputMode = 0x03
  TriggerElapsedTime = 0x04
  LowEnergy = 0x08
  SPI = 0x10
  NFCConf = 0x21
  PlayerLight = 0x30
  HomeLight = 0x38
  IMU = 0x40
  Vibration = 0x48


class SPICommand(Enum):
  SerialNumber = b"\x00\x60"
  ControllerColor = b"\x50\x60"
  FactorySensorStick = b"\x80\x60"
  FactoryStick = b"\x98\x60"
  FactoryCalibration2 = b"\x3d\x60"
  UserCalibration = b"\x10\x80"
  MotionCalibration = b"\x28\x80"
  FactoryCalibration1 = b"\x20\x60"

class RequestMessage:
  @classmethod
  def parse(self, message):
    parsed = RequestMessage()
    parsed.command = MessageCommand(message[0])

    if parsed.command == MessageCommand.Setup:
      parsed.subcommand = SetupMessageSubcommand(message[1])
    elif parsed.command == MessageCommand.UART and len(message) > 16:
      parsed.subcommand = UARTMessageSubcommand(message[10])
      parsed.timer = message[1]
      parsed.data = message[11:]
      if parsed.subcommand == UARTMessageSubcommand.SPI:
        parsed.spi_command = SPICommand(message[11:13])
        parsed.spi_len = message[15]
        parsed.data = message[16:]

    return parsed
  
  def __init__(self):
    self.command = None
    self.subcommand = None
    self.spi_command = None
    self.spi_len = None
    self.data = None
    self.timer = None


class ResponseFactory:
  def __init__(self, controller): 
    self.controller = controller

  def response_for_controller(self, timer = 0):
    buffer = bytes.fromhex(self.controller.state_hex())
    return self.make_response(0x30, timer, buffer)

  def response_for_request(self, request, timer = 0):
    if request.command == MessageCommand.Setup:
      if request.subcommand == SetupMessageSubcommand.MacAddrRequest:
        return self.make_response(0x81, request.subcommand.value, bytes.fromhex("0003" + self.controller.reverse_mac_address_hex()))
      elif request.subcommand == SetupMessageSubcommand.Handshake:
        return self.make_response(0x81, request.subcommand.value, [])
    elif request.command == MessageCommand.UART:
      if request.subcommand == UARTMessageSubcommand.BluetoothPairing:
        return self.make_uart_response(0x81, request.subcommand.value, [0x03], timer)
      elif request.subcommand == UARTMessageSubcommand.DeviceInfo:
        return self.make_uart_response(0x82, request.subcommand.value, bytes.fromhex("03480302" + self.controller.mac_address_hex() + "0101"), timer)
      elif request.subcommand == UARTMessageSubcommand.InputMode or request.subcommand == UARTMessageSubcommand.LowEnergy or request.subcommand == UARTMessageSubcommand.PlayerLight or request.subcommand == UARTMessageSubcommand.HomeLight or request.subcommand == UARTMessageSubcommand.IMU or request.subcommand == UARTMessageSubcommand.Vibration:
        return self.make_uart_response(0x80, request.subcommand.value, [], timer)
      elif request.subcommand == UARTMessageSubcommand.TriggerElapsedTime:
        return self.make_uart_response(0x83, request.subcommand.value, [], timer)
      elif request.subcommand == UARTMessageSubcommand.NFCConf:
        return self.make_uart_response(0xa0, request.subcommand.value, bytes.fromhex("0100ff0003000501000000000000000000000000000000000000000000000000005c"), timer)
      elif request.subcommand == UARTMessageSubcommand.SPI:
        if request.spi_command == SPICommand.SerialNumber:
          return self.make_spi_response(request.spi_command.value, bytes.fromhex("ffffffffffffffffffffffffffffffff"), timer)
        elif request.spi_command == SPICommand.ControllerColor:
          return self.make_spi_response(request.spi_command.value, bytes.fromhex(self.controller.color), timer)
        elif request.spi_command == SPICommand.FactorySensorStick:
          return self.make_spi_response(request.spi_command.value, bytes.fromhex("50fd0000c60f0f30619630f3d41454411554c7799c333663"), timer)
        elif request.spi_command == SPICommand.FactoryStick:
          return self.make_spi_response(request.spi_command.value, bytes.fromhex("0f30619630f3d41454411554c7799c333663"), timer)
        elif request.spi_command == SPICommand.FactoryCalibration2:
          return self.make_spi_response(request.spi_command.value, bytes.fromhex("21466359887c75e665d16779320665053664ff323232ffffff"), timer)
        elif request.spi_command == SPICommand.FactoryCalibration1:
          return self.make_spi_response(request.spi_command.value, bytes.fromhex("3500a0fe5d01004000400040d7ffceffc1ff3b343b343b34"), timer)
        elif request.spi_command == SPICommand.UserCalibration:
          return self.make_spi_response(request.spi_command.value, bytes.fromhex("ffffffffffffffffffffffffffffffffffffffffffffffff"), timer)
        elif request.spi_command == SPICommand.MotionCalibration:
          return self.make_spi_response(request.spi_command.value, bytes.fromhex("beff3e00f001004000400040fefffeff0800e73be73be73b"), timer)

    return b""

  def make_spi_response(self, address, data, timer):
    buf = bytearray(address)
    buf.extend([0x00, 0x00])
    buf.append(len(data))
    buf.extend(data)
    
    return self.make_uart_response(0x90, 0x10, buf, timer)

  def make_uart_response(self, code, subcommand, data, timer):
    buf = bytearray.fromhex(self.controller.state_hex())
    buf.extend([code, subcommand])
    buf.extend(data)

    return self.make_response(0x21, timer, buf)

  def make_response(self, command, subcommand, data):
    buffer = bytearray([command, subcommand])
    buffer.extend(data)
    padding = bytearray(64-len(buffer))
    buffer.extend(padding)
    return buffer