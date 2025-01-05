import serial
import time
import re
import sys
import json

# Serial port configuration
port = "/dev/ttyACM0"
baud_rate = 38400


def read_epc():
    # Hexadecimal representation of the epc command
    # command_tid = b'\x0A\x52\x32\x2C\x30\x2C\x36\x0D'  # Corresponds to <LF>R2,0,6<CR>
    command_epc = b'\x0A\x51\x0D'
    # command_multi_epc = b'\x0A\x55\x0D'

    # Adjusted TID pattern: matches 'R' followed by 'E2' and 24 hex characters
    # tid_pattern = re.compile(r"^R(E2[0-9A-F]{22})$")
    epc_pattern = re.compile(r'^Q([0-9A-F]+)$')  # Regex to match "Q" followed by alphanumeric characters (EPC)

    # Open the serial port
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)  # 1 second timeout
        # print(f"Serial port {port} opened at {baud_rate} baud.")
    except serial.SerialException as e:
        # print(f"Failed to open serial port: {e}")
        return json.dumps({"error": f"Failed to open serial port: {e}"})

    # Loop until the epc is received
    epc_received = None
    try:
        while epc_received is None:
            # Send the command
            ser.write(command_epc)
            # print("Command sent: <LF>R2,0,6<CR>")

            # Wait for the response
            response = ser.readline().strip()  # Read a line and strip whitespace
            # print(f"Raw response: {response}")  # Debugging: Show the raw response bytes

            # Decode to a string for matching
            try:
                response_str = response.decode('ascii', errors='ignore')  # Decode to ASCII
                # print(f"Decoded response: {response_str}")  # Debugging: Show the decoded response
            except Exception as e:
                # print(f"Error decoding response: {e}")
                continue  # Skip this iteration if decoding fails

            if response_str:
                match = epc_pattern.match(response_str)
                if match:
                    # Extract the epc from the matched pattern
                    epc_received = match.group(1)  # Group 1 corresponds to 'E2[0-9A-F]{24}'
                    # print(f"epc received: {epc_received}")
                elif response_str == "R":
                    # Device returned only the command, indicating no data
                    None
                    # print("No epc received. Retrying...")
                else:
                    # Response does not match expected formats
                    None
                    # print("Unexpected response. Retrying...")

            time.sleep(0.1)  # Wait 1 second before retrying
    finally:
        ser.close()
        # print("Serial port closed.")

    if epc_received:
        # print(f"Queried epc: {epc_received}")
        return json.dumps({"epc": epc_received})  # Return the epc as JSON
    else:
        return json.dumps({"error": "No valid EPC received."})  # Return an error message


# Execute the function and output the result
epc = read_epc()
print(epc)  # Print the result (this will be picked up by Flask)
sys.exit(0)
