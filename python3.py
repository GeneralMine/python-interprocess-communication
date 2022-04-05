#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python3 using two named pipes (I/O)

import os
import time
import json

pipe_name_command = "~/pipe_test_command"
pipe_name_telemetry = "~/pipe_test_telemetry"
commands = [
    {
        "channel": "function",
        "type": "aquire",
        "payload" : 1
    },
    {
        "channel": "control",
        "type": "takeoff",
        "payload" : 10
    },
    {
        "channel": "control",
        "type": "move",
        "payload" : [1,2,3]
    },
    {
        "channel": "control",
        "type": "land",
        "payload" : 0
    },
    {
        "channel": "function",
        "type": "free",
        "payload" : 0
    }
]

# Command: Write Pipe
if not os.path.exists(pipe_name_command):
    os.mkfifo(pipe_name_command)
commandPipe = os.open(pipe_name_command, os.O_WRONLY)
commandCounter = 0

# Telemetry: Read Pipe
if not os.path.exists(pipe_name_telemetry):
    os.mkfifo(pipe_name_telemetry)
telemetryPipe = open(pipe_name_telemetry, "r")
telemetryCounter = 0

# Loop
while True:
    # Telemetry: Read
    line = json.loads(telemetryPipe.readline()[:-1])
    print("[Receive][Number %04d] Telemetry from Python2: %s\n" % (telemetryCounter, line["debug"]))
    telemetryCounter = telemetryCounter + 1

    # Command: Write
    msg = (json.dumps(commands[commandCounter % len(commands)]) + "\n").encode("utf-8")
    os.write(commandPipe, msg)
    print("[Sending][Number %04d] Command to Python2\n" % commandCounter)
    commandCounter = commandCounter + 1

    # Delay
    time.sleep(1)
