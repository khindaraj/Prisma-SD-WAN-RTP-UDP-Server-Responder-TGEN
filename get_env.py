#!/usr/bin/env python3

import os
import time
import random

random.seed()

# Generate random delay between 0 and 6 seconds
delay = random.uniform(0, 6)

# Simulate the delay
time.sleep(delay)

# Print headers for a basic HTML response
print("Content-type: text/html\r\n\r\n")

# Print message with the delay value
print(f"Delayed response by {delay} seconds")

# Print environment information
print("<font size=+1>Environment</font><br>")
for param, value in os.environ.items():
    # Improved formatting with f-strings and alignment
    print(f"<b>{param:20s}</b>: {value}<br>")
