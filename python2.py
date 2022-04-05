#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Python2 using two named pipes (I/O)

import os
import time
import json

pipe_name_command = "~/pipe_test_command"
pipe_name_telemetry = "~/pipe_test_telemetry"
telemetry = json.load(open("telemetry.json"))

# Command: Read Pipe
if not os.path.exists(pipe_name_command):
    os.mkfifo(pipe_name_command)
commandPipe = open(pipe_name_command, "r")
commandCounter = 0

# Telemetry: Write Pipe
if not os.path.exists(pipe_name_telemetry):
    os.mkfifo(pipe_name_telemetry)
telemetryPipe = os.open(pipe_name_telemetry, os.O_WRONLY)
telemetryCounter = 0

# Loop
while True:
    # Telemetry: Write
    telemetry["debug"] = "Frame %04d" % telemetryCounter
    msg = (json.dumps(telemetry) + "\n").encode("utf-8")
    os.write(telemetryPipe, msg)
    print("[Sending][Number %04d] Telemetry to Python3\n" % telemetryCounter)
    telemetryCounter = telemetryCounter + 1

    # Command: Read
    line = json.loads(commandPipe.readline()[:-1])
    print("[Receive][Number %04d] Command from Python3: %s\n" % (commandCounter, line["type"]))
    commandCounter = commandCounter + 1

    # Delay
    time.sleep(1)
