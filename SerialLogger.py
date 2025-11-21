# Jatin Gandhi., 
# This script logs Arduino analog input A0 and A1 into CSV  file 
# Arduino firmware code to stream the data is at the end of the file in doc string

import serial
import csv
from datetime import datetime

# --- User settings ---
PORT = 'COM61'         # <- change this to your Arduino port (e.g. '/dev/ttyACM0' on Linux)
BAUD = 1_000_000      # matches Serial.begin(1000000)
OUTPUT_FILE = 'dso_data.csv'

# --- Setup serial port ---
try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except:
    print(f"Error: Could not open serial port {PORT}")
    exit(1)

# --- Open CSV file for writing ---
with open(OUTPUT_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'A0', 'A1'])  # header row

    print(f"Recording data from {PORT} at {BAUD} baud...")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            # Expect format: "value0,value1"
            parts = line.split(',')
            if len(parts) == 2:
                try:
                    a0 = int(parts[0])
                    a1 = int(parts[1])
                    t = datetime.now().isoformat(timespec='milliseconds')
                    writer.writerow([t, a0, a1])
                    f.flush();
                except ValueError:
                    pass  # ignore malformed lines
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        ser.close()
        print(f"Data saved to {OUTPUT_FILE}")


"""

// Arduino Uno R4 Minima based firmware to stream the data
// ------------------------------------------------------
// UNO R4 Minima - Dual analog sampler, CSV @ 1,000,000 baud
// ------------------------------------------------------

const int CH0 = A0;
const int CH1 = A1;

void setup() {
  Serial.begin(1000000);
  analogReadResolution(12);   // UNO R4 supports up to 12-bit ADC
}

void loop() {
  uint16_t a0 = analogRead(CH0);
  uint16_t a1 = analogRead(CH1);

  // Comma-separated output
  Serial.print(a0);
  Serial.print(',');
  Serial.println(a1);
}

"""
