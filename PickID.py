import gpiozero
import time

# --- GPIO Pin Configuration ---
# Use BCM mode for GPIO pin numbering (default for gpiozero)
# Define the GPIO pins for each locker element from 1 to 4
GPIO_PINS = {
    1: 21,  # Pick_ID[1] corresponds to GPIO 21
    2: 20,  # Pick_ID[2] corresponds to GPIO 20
    3: 16,  # Pick_ID[3] corresponds to GPIO 16
    4: 12   # Pick_ID[4] corresponds to GPIO 12
}

# --- Initialize Input Pins ---
# For gpiozero, we create InputDevice objects.
# The 'pull_up=True' argument enables the internal pull-up resistor.
# This means:
# - If the pin is floating or connected to high, it reads True (1)
# - If the pin is connected to ground, it reads False (0)
# This matches your desired logic where HIGH=1 (in use) and LOW=0 (available).
input_devices = {}
for i, pin_num in GPIO_PINS.items():
    try:
        input_devices[i] = gpiozero.InputDevice(pin_num, pull_up=True)
        print(f"GPIO {pin_num} configured as input with pull-up.")
    except gpiozero.GPIODeviceError as e:
        print(f"Error initializing GPIO {pin_num}: {e}")
        print("Please ensure the pin is correct and gpiozero has permissions.")
        # If any pin fails, we might want to exit or handle gracefully
        exit() # Exiting for critical errors in this example

# --- Pick_ID Array ---
# Initialize the Pick_ID array with 5 elements.
# Pick_ID[0] will be the calculated result (index of first available locker).
# Pick_ID[1] through Pick_ID[4] will be the status read from GPIO.
Pick_ID = [0, 0, 0, 0, 0] # Initialize with -1 for element 0 and 0 for others

print("Starting GPIO status reading with gpiozero. Press Ctrl+C to exit.")

try:
    while True:
        # Read the status of GPIO pins and update Pick_ID[1] through Pick_ID[4]
        for i in range(1, 5):
            # input_devices[i].value returns True (1) if HIGH, False (0) if LOW
            # We map True to 1 (in use) and False to 0 (available)
            Pick_ID[i] = 0 if input_devices[i].value else 1
        
        # --- Calculate value for Pick_ID[0] ---
        # Find the index (from 1 to 4) of the first locker with status 0 (available).
        # If no locker has status 0, Pick_ID[0] will be -1.
        found_available_locker = False
        for i in range(1, 5):
            if Pick_ID[i] == 0:
                Pick_ID[0] = i  # Store the index of the available locker
                found_available_locker = True
                break
        
        if not found_available_locker:
            Pick_ID[0] = 0 # No lockers available
        
        # Print the current status of the Pick_ID array
        print(f"Pick_ID: {Pick_ID}")

        time.sleep(1) # Wait 1 second before reading again

except KeyboardInterrupt:
    # Handle user pressing Ctrl+C to exit
    print("\nProgram stopped.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # gpiozero automatically handles cleanup when script exits or objects go out of scope,
    # but explicitly closing can be good practice if your script has complex flow.
    for device in input_devices.values():
        device.close()
    print("GPIO devices closed.")

