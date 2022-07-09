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
  Unknown1 = 0x38
  IMU = 0x40
  Vibration = 0x48


class SPICommand(Enum):
  SerialNumber = b"\x00\x60"
  ControllerColor = b"\x50\x60"
  FactorySensorStick = b"\x80\x60"
  FactoryStick = b"\x98\x60"
  FactoryCalibration = b"\x3d\x60"
  UserCalibration = b"\x10\x80"
  MotionCalibration = b"\x28\x80"
  Unknown1 = b"\x20\x60"

class RequestMessage:
  @classmethod
  def parse(self, message):
    parsed = Message()
    parsed.command = MessageCommand(message[0])

    if parsed.command == MessageCommand.Setup:
      parsed.subcommand = SetupMessageSubcommand(message[1])
    else:
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