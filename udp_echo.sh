#!/usr/bin/env bash

# Get the script directory from the first argument
SCRIPT_DIR="$1"

# Check if an argument is provided (script directory)
if [[ -z "$SCRIPT_DIR" ]]; then
  echo "Error: Please provide the script directory as the first argument."
  echo "Usage: $0 <script_directory>"
  exit 1
fi

# Check if the script directory exists
if [[ ! -d "$SCRIPT_DIR" ]]; then
  echo "Error: Script directory '$SCRIPT_DIR' does not exist."
  exit 1
fi

# Change directory to the script directory
cd "$SCRIPT_DIR" || exit 1

# Run the Python script in the background with error handling
# Replace "udp_echo.py" with the actual script name
"$SCRIPT_DIR/udp_echo.py" &

# Optionally capture the background process ID (PID)
# pid=$!  # Uncomment this line to capture the PID

# Log successful execution (optional)
#echo "Started udp_echo.py in the background."

# Optionally detach from the terminal session (use with caution)
# disown  # Uncomment this line to detach completely

exit 0

