from flask import Flask, jsonify, request
from controller_setup.controller import SwitchController
from threading import Timer, Thread
from time import time
from math import sin, cos, pi
from socket_coordinator import SocketCoordinator

controller = SwitchController()
coordinator = SocketCoordinator(controller)
app = Flask(__name__)

@app.post("/api/v1/socket/start")
def start_socket():
  global coordinator
  coordinator.start()
  return "", 204

@app.get("/api/v1/controller")
def get_controller():
  global controller
  return jsonify(controller.state.__dict__)

@app.post("/api/v1/press")
def set_controller_state():
  global controller
  time = request.json["time"]
  buttons = request.json["buttons"]
  for button in buttons:
    controller.state.__dict__[button] = True
  Timer(time, _reset_buttons, [buttons]).start()
  return jsonify(controller.state.__dict__)

@app.post("api/v1/move")
def move_stick():
  global controller
  analog_stick = request.json["stick"]
  [position_x, position_y] = request.json["position"]
  controller.state.__dict__[f"{analog_stick}_stick_x"] = position_x
  controller.state.__dict__[f"{analog_stick}_stick_y"] = position_y
  return jsonify(controller.state.__dict__)

@app.post("/api/v1/roll")
def roll_analog_stick():
  global controller
  stick = request.json["stick"]
  duration = request.json["duration"]
  frequency = request.json["frequency"]
  Thread(target=_roll_thread_method, args=[stick, duration, frequency]).start()
  return jsonify(controller.state.__dict__)


def _reset_buttons(buttons):
  global controller
  for button in buttons:
    controller.state.__dict__[button] = False

def _roll_thread_method(analog_stick, duration, frequency):
  global controller
  start = time()
  end = time()
  while end-start < duration:
    elapsed = end-start
    controller.state.__dict__[f"{analog_stick}_stick_x"] = cos(2*pi*frequency*elapsed)
    controller.state.__dict__[f"{analog_stick}_stick_y"] = sin(2*pi*frequency*elapsed)
    end = time()
  controller.state.__dict__[f"{analog_stick}_stick_x"] = 0
  controller.state.__dict__[f"{analog_stick}_stick_y"] = 0

app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
