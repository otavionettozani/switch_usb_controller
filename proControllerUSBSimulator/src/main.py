from flask import Flask, jsonify, request
from controller_setup.controller import SwitchController
from threading import Timer, Thread
from time import time
from math import sin, cos, pi

controller = SwitchController()

app = Flask(__name__)

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