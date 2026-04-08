#!/usr/bin/env python3 -u
import subprocess
import os
import gpiod
import gpiodevice
from gpiod.line import Bias, Direction, Edge

# GPIO pins for buttons A, B, C, D (top to bottom)
BUTTONS = [5, 6, 16, 24]
LABELS  = ["A", "B", "C", "D"]

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
VENV_PYTHON = os.path.expanduser("~/.virtualenvs/pimoroni/bin/python3")

def run_script(script_name):
    print(f"Running {script_name}...")
    subprocess.run([VENV_PYTHON, os.path.join(SCRIPT_DIR, script_name)], cwd=SCRIPT_DIR)
    print(f"{script_name} finished.")

INPUT = gpiod.LineSettings(
    direction=Direction.INPUT,
    bias=Bias.PULL_UP,
    edge_detection=Edge.FALLING
)

chip    = gpiodevice.find_chip_by_platform()
OFFSETS = [chip.line_offset_from_id(id) for id in BUTTONS]
request = chip.request_lines(
    consumer="inky-buttons",
    config=dict.fromkeys(OFFSETS, INPUT)
)

print("Button monitor running. Press Ctrl+C to exit.")
print("  Button A (top) → guest_wifi.py")
print("  Button B       → inky_app.py")

# Drain any events that accumulated before the script started
while request.wait_edge_events(0):
    request.read_edge_events()

last_button = None

while True:
    for event in request.read_edge_events():
        index = OFFSETS.index(event.line_offset)
        label = LABELS[index]
        print(f"Button {label} pressed.")

        if label == "A":
            if last_button != "A":
                last_button = "A"
                run_script("guest_wifi.py")
            else:
                print("Button A already active, ignoring.")

        if label == "B":
            if last_button != "B":
                last_button = "B"
                run_script("inky_app.py")
            else:
                print("Button B already active, ignoring.")
