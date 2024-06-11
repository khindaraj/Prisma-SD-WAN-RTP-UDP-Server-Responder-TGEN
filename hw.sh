#!/bin/bash

# Generate random delay between 0 and 5 seconds (inclusive)
myrand=$(awk -v min=0 -v max=5 'BEGIN{srand(); print int(min + rand() * (max - min + 1))}')

# Simulate delay
sleep "$myrand"

# Print HTML headers
printf "Content-type: text/html\n\n"

# Print message and delay information
printf "Hello World!\n"
printf "Delayed for %d seconds\n" "$myrand"
