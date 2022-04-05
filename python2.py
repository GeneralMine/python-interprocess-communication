#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Python2 using two named pipes (I/O)

import os
import sys
import time
import json

pipe_name_command = "/home/generalmine/pipe_test_command"
pipe_name_telemetry = "/home/generalmine/pipe_test_telemetry"
version = sys.version_info
telemetry = json.load(open("telemetry.json"))

# Command
if not os.path.exists(pipe_name_command):
    os.mkfifo(pipe_name_command)
commandPipe = open(pipe_name_command, "r")
commandCounter = 0

# Telemetry
if not os.path.exists(pipe_name_telemetry):
    os.mkfifo(pipe_name_telemetry)
telemetryPipe = os.open(pipe_name_telemetry, os.O_WRONLY)
telemetryCounter = 0

# Loop
while True:
    # Telemetry
    telemetry["debug"] = "Frame %04d" % telemetryCounter
    msg = (json.dumps(telemetry) + "\n").encode("utf-8")
    os.write(telemetryPipe, msg)
    print("[Sending][Number %04d] Telemetry to Python3\n" % telemetryCounter)
    telemetryCounter = telemetryCounter + 1

    # Command
    line = json.loads(commandPipe.readline()[:-1])
    print("[Receive][Number %04d] Command from Python3: %s\n" % (commandCounter, line["type"]))
    commandCounter = commandCounter + 1

    # Delay
    time.sleep(1)
