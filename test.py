import tkinter as tk
from tkinter import ttk
import sys

# Try importing gpiozero. If not available, run in simulation mode.
try:
    from gpiozero import OutputDevice, InputDevice
    GPIO_AVAILABLE = True
    print("gpiozero loaded successfully. GPIO functions enabled.")
except ImportError:
    print("gpiozero not found. Running in simulation mode.")
    GPIO_AVAILABLE = False
except Exception as e:
    print(f"Error loading gpiozero: {e}. Running in simulation mode.")
    GPIO_AVAILABLE = False

# --- GPIO Configuration ---
# GPIO pins to control (using BCM numbering)
OUTPUT_GPIO_PINS = [1, 7, 8, 25]

# Input pins for locker status (Sensor Input)
# Locker 1: GPIO 21, Locker 2: GPIO 20, Locker 3: GPIO 16, Locker 4: GPIO 12
INPUT_GPIO_PINS = {
    1: 21,
    2: 20,
    3: 16,
    4: 12
}
LOCKER_COUNT = len(INPUT_GPIO_PINS)

# --- Initialize GPIO Output Devices ---
outputs = []
input_devices = {}

if GPIO_AVAILABLE:
    try:
        for pin in OUTPUT_GPIO_PINS:
            output_device = OutputDevice(pin, initial_value=False) # Default to LOW
            outputs.append(output_device)
            print(f"Successfully initialized Output GPIO {pin}")
    except Exception as e:
        print(f"Error initializing Output GPIO pin: {e}. Disabling GPIO.")
        GPIO_AVAILABLE = False # Disable GPIO if any output error occurs

    try:
        if GPIO_AVAILABLE: # Only proceed if outputs initialized without error
            for locker_id, pin in INPUT_GPIO_PINS.items():
                # Use pull_up=False to read normal HIGH/LOW signals without internal pull-up
                input_devices[locker_id] = InputDevice(pin, pull_up=False) 
                print(f"Successfully initialized Input GPIO {pin} for Locker {locker_id} with pull_up=False")
    except Exception as e:
        print(f"Error initializing Input GPIO pin: {e}. Disabling GPIO.")
        GPIO_AVAILABLE = False # Disable GPIO if any input error occurs
else:
    print("GPIO not available. All GPIO interactions will be simulated.")


# --- Button Event Handlers ---
def on_button_press(output_index, button_name):
    """
    When a GUI button is pressed, set the corresponding GPIO output pin to HIGH (or simulate).
    """
    if GPIO_AVAILABLE:
        if 0 <= output_index < len(outputs):
            outputs[output_index].on()
            print(f"'{button_name}' pressed: Actual GPIO {OUTPUT_GPIO_PINS[output_index]} -> HIGH")
    else:
        print(f"SIMULATION: '{button_name}' pressed. (Would set GPIO {OUTPUT_GPIO_PINS[output_index]} to HIGH)")

def on_button_release(output_index, button_name):
    """
    When a GUI button is released, set the corresponding GPIO output pin to LOW (or simulate).
    """
    if GPIO_AVAILABLE:
        if 0 <= output_index < len(outputs):
            outputs[output_index].off()
            print(f"'{button_name}' released: Actual GPIO {OUTPUT_GPIO_PINS[output_index]} -> LOW")
    else:
        print(f"SIMULATION: '{button_name}' released. (Would set GPIO {OUTPUT_GPIO_PINS[output_index]} to LOW)")

# --- Set up the GUI Window ---
print("Starting GUI setup...")
root = tk.Tk()
root.title("GPIO Control & Input Status")

# --- Set to full-screen mode ---
root.attributes('-fullscreen', False) 

# --- Add Escape key binding to exit full-screen ---
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)
    # Optional: uncomment the line below to close the application when exiting full-screen
    # root.destroy() 
root.bind('<Escape>', exit_fullscreen)


# Main frame for padding and overall layout
main_frame = ttk.Frame(root, padding="15")
main_frame.pack(expand=True, fill="both")

# Title Label
ttk.Label(main_frame, text="Raspberry Pi GPIO Control Panel", 
          font=('Arial', 18, 'bold'), anchor='center').pack(pady=(0, 20), fill="x")

# Content frame to hold main sections (stacked vertically)
content_frame = ttk.Frame(main_frame)
content_frame.pack(expand=True, fill="both")

# --- Output Control Section (Top Part) ---
output_frame = ttk.LabelFrame(content_frame, text="Output Control", padding="15")
output_frame.pack(side="top", fill="both", expand=True, pady=(0, 15))

button_names = ["Locker 1 Output (GPIO 1)", "Locker 2 Output (GPIO 7)", 
                "Locker 3 Output (GPIO 8)", "Locker 4 Output (GPIO 25)"]

for i in range(LOCKER_COUNT): 
    # --- Adjusted: Reduced horizontal size (width) ---
    button = ttk.Button(output_frame, text=f"{button_names[i]}", width=50) 
    button.bind("<Button-1>", lambda event, idx=i, btn_name=button_names[i]: on_button_press(idx, btn_name))
    button.bind("<ButtonRelease-1>", lambda event, idx=i, btn_name=button_names[i]: on_button_release(idx, btn_name))
    # --- Adjusted: Increased vertical size (pady) ---
    button.pack(pady=12, padx=5, fill="x")

# --- Input Status Section (Bottom Part) ---
input_status_frame = ttk.LabelFrame(content_frame, text="Input Status", padding="15")
input_status_frame.pack(side="bottom", fill="both", expand=True, pady=(15, 0))

# Variables to store status labels for each locker
locker_status_labels = {} 

for i in range(LOCKER_COUNT): 
    locker_id = i + 1 

    # Frame for each input row (Locker ID + Status Indicator)
    input_row_frame = ttk.Frame(input_status_frame)
    input_row_frame.pack(pady=12, fill="x", anchor="w")

    # Locker ID Label
    ttk.Label(input_row_frame, text=f"Locker {locker_id}:", font=('Arial', 12, 'bold')).pack(side="left", padx=(0, 15))

    # Status Indicator (Rectangle)
    status_label = tk.Label(input_row_frame, text="N/A", 
                            font=('Arial', 12, 'bold'), # Increased font size
                            width=10, height=2, 
                            relief="solid", borderwidth=1, bg="gray", fg="white")
    status_label.pack(side="left", padx=(0,5)) 
    
    # Store the status_label widget for later updates
    locker_status_labels[locker_id] = status_label

print("GUI elements created. Starting update loop...")

# --- Function to update Input Status Display ---
def update_input_status_display():
    if GPIO_AVAILABLE:
        for locker_id, device in input_devices.items():
            status_label = locker_status_labels[locker_id]
            if device.value: # If GPIO is HIGH
                status_label.config(text="FILLED", bg="red") 
            else: # If GPIO is LOW
                status_label.config(text="EMPTY", bg="green")
    else:
        # Simulation/Mock mode if GPIO is not available
        for locker_id in range(1, LOCKER_COUNT + 1):
            status_label = locker_status_labels[locker_id]
            current_text = status_label.cget("text") 
            if "OPEN" in current_text: 
                status_label.config(text="EMPTY (Mock)", bg="green")
            else: 
                status_label.config(text="FILLED (Mock)", bg="red")

    root.after(500, update_input_status_display) # Schedule the next update every 500ms

# Initial call to start the input status display update loop
update_input_status_display()

print("Entering Tkinter main loop.")
# --- Run the Tkinter event loop ---
root.mainloop()
print("Tkinter main loop exited.")