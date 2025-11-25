import tkinter as tk
import serial
import threading
import time
import random

# Adjust COM port and baud rate
SERIAL_PORT = 'COM3'   # or '/dev/ttyUSB0' on Linux/Mac
BAUD_RATE = 9600

# Map sensor values (e.g. 0–1023) to 0–180 degrees for arc extent
def map_sensor_value(value, in_min=0, in_max=1023, out_min=0, out_max=360):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

class ArcDisplayApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack()

        # Draw initial arc
        #drawstyle = tk.PIESLICE;
        drawstyle = tk.ARC;
        #drawstyle = tk.CHORD;
        self.arc = self.canvas.create_arc(50, 50, 250, 250,
                                          start=90, extent=0,
                                          fill="blue", outline="skyblue",
                                          width=2, style=drawstyle)

        # Setup serial
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

        # Start reading thread
        if self.ser:
            threading.Thread(target=self.read_serial_simulation, daemon=True).start()

    def update_arc(self, sensor_val):
        angle = map_sensor_value(sensor_val)
        self.canvas.itemconfig(self.arc, extent=angle)


    def read_serial_simulation(self):
        while True:
            try:
                sensor_val = random.randint(0, 1024);
                # Update arc on main UI thread
                self.root.after(0, self.update_arc, sensor_val)
                time.sleep(0.2);
            except Exception as e:
                print("Error reading from serial:", e)

    def read_serial(self):
        while True:
            try:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode().strip()
                    if line.isdigit():
                        sensor_val = int(line)
                        # Update arc on main UI thread
                        self.root.after(0, self.update_arc, sensor_val)
            except Exception as e:
                print("Error reading from serial:", e)

# Main Tkinter loop
root = tk.Tk()
root.title("Sensor Arc Display")
app = ArcDisplayApp(root)
root.mainloop()
