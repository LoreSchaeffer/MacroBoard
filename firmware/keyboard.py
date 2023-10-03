import machine
import utime

# Define rows and columns
rows = [machine.Pin(11, machine.Pin.OUT), machine.Pin(10, machine.Pin.OUT), machine.Pin(9, machine.Pin.OUT), machine.Pin(8, machine.Pin.OUT)]
cols = [machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP), machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP), machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP), machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)]

# Define a keypad matrix
keypad = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Variable to keep track of the key state
last_key = None

# Function to read input from the keypad matrix
def read_key():
    global last_key
    for i in range(4):
        # Activate a single row as a low output
        rows[i].value(0)
        
        # Scan all columns to detect a pressed key
        for j in range(4):
            if not cols[j].value():
                # Check if the key is different from the last pressed key
                if keypad[i][j] != last_key:
                    # Wait for a brief moment to avoid button bounce
                    utime.sleep_ms(10)
                    
                    # Check again if the key is still pressed
                    if not cols[j].value():
                        # Store the pressed key and return it
                        last_key = keypad[i][j]
                        return last_key
            else:
                # Detect key release
                last_key = None
        
        # Deactivate the row
        rows[i].value(1)
    
    # No key pressed
    return None

# Example usage
while True:
    key = read_key()
    if key is not None:
        print("Key pressed:", key)