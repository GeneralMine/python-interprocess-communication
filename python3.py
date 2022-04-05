#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python3 using two named pipes (I/O)

import os
import time
import json

pipe_name_command = "/tmp/pipe_test_command"
pipe_name_telemetry = "/tmp/pipe_test_telemetry"
commands = json.load(open("commands.json"))
telemetryCounter = 0
commandCounter = 0

# Create Pipes if not exists
if not os.path.exists(pipe_name_command):
    os.mkfifo(pipe_name_command)
if not os.path.exists(pipe_name_telemetry):
    os.mkfifo(pipe_name_telemetry)

# Command: Write Pipe
commandPipe = os.open(pipe_name_command, os.O_WRONLY)

# Telemetry: Read Pipe
telemetryPipe = open(pipe_name_telemetry, "r")

# Loop
while True:
    # Telemetry: Read
    line = json.loads(telemetryPipe.readline()[:-1])
    print("[Receive][Number %04d] Telemetry from Python2: %s\n" % (telemetryCounter, line["debug"]))
    telemetryCounter += 1

    # Command: Write
    commands[1]["payload"] = str(commandCounter)
    msg = (json.dumps(commands[commandCounter % len(commands)]) + "\n").encode("utf-8")
    os.write(commandPipe, msg)
    print("[Sending][Number %04d] Command to Python2\n" % commandCounter)
    commandCounter += 1

    # Delay
    time.sleep(1)
