#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Python2 using two named pipes (I/O)

import os
import time
import json

pipe_name_command = "/tmp/pipe_test_command"
pipe_name_telemetry = "/tmp/pipe_test_telemetry"
telemetry = json.load(open("telemetry.json"))
telemetryCounter = 0
commandCounter = 0

# Create Pipes if not exists
if not os.path.exists(pipe_name_command):
    os.mkfifo(pipe_name_command)
if not os.path.exists(pipe_name_telemetry):
    os.mkfifo(pipe_name_telemetry)

# Command: Read Pipe
commandPipe = open(pipe_name_command, "r")

# Telemetry: Write Pipe
telemetryPipe = os.open(pipe_name_telemetry, os.O_WRONLY)

# Loop
while True:
    # Telemetry: Write
    telemetry["debug"] = "Frame %04d" % telemetryCounter
    msg = (json.dumps(telemetry) + "\n").encode("utf-8")
    os.write(telemetryPipe, msg)
    print("[Sending][Number %04d] Telemetry to Python3\n" % telemetryCounter)
    telemetryCounter += 1

    # Command: Read
    line = json.loads(commandPipe.readline()[:-1])
    print("[Receive][Number %04d] Command from Python3: %s\n" % (commandCounter, line["type"] + ":" + line["payload"]))
    commandCounter += 1

    # Delay
    time.sleep(1)
