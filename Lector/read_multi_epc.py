import serial
import time
import re
import sys
import json

# Serial port configuration
port = "/dev/ttyACM0"
baud_rate = 38400

def read_multi_epc():
    # Hexadecimal representation of the multi-epc command
    command_multi_epc = b'\x0A\x55\x0D'

    # Regex to match "Q" followed by alphanumeric characters (EPCs)
    epc_pattern = re.compile(r'^U([0-9A-F]+)$')

    # Open the serial port
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
    except serial.SerialException as e:
        return json.dumps({"error": f"Failed to open serial port: {e}"})

    # Initialize variables
    detected_epcs = set()  # Use a set to avoid duplicates
    start_time = time.time()  # Record the start time

    try:
        while time.time() - start_time < 10:  # Run for 10 seconds
            # Send the command
            ser.write(command_multi_epc)

            # Wait for the response
            response = ser.readline().strip()  # Read a line and strip whitespace

            # Decode to a string for matching
            try:
                response_str = response.decode('ascii', errors='ignore')
            except Exception as e:
                continue  # Skip this iteration if decoding fails

            # Check if the response matches the EPC pattern
            match = epc_pattern.match(response_str)
            if match:
                # Add the EPC to the set
                detected_epcs.add(match.group(1))
                # print("EPC detected "+match.group(1))

            # Small delay to avoid overwhelming the device
            time.sleep(0.1)

    finally:
        ser.close()

    # Return the collected EPCs as a JSON object
    if detected_epcs:
        return json.dumps({"epcs": list(detected_epcs)})
    else:
        return json.dumps({"error": "No valid EPCs detected."})

# Execute the function and output the result
if __name__ == "__main__":
    result = read_multi_epc()
    print(result)
    sys.exit(0)
