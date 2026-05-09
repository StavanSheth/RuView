"""Force reset ESP32 via RTS and read boot logs from COM10."""
import serial
import time
import sys
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

port = sys.argv[1] if len(sys.argv) > 1 else "COM10"
baud = 115200

print(f"Opening {port}...")
try:
    s = serial.Serial(port, baud, timeout=1)
    print("Opened. Forcing reset via RTS/DTR...")

    # Hard reset: pull EN low then release
    s.setDTR(False)
    s.setRTS(True)
    time.sleep(0.2)
    s.setRTS(False)
    time.sleep(0.1)
    s.setDTR(True)
    time.sleep(0.05)
    s.setDTR(False)

    print("Reset sent. Reading boot logs for 20 seconds...\n")
    end = time.time() + 20
    while time.time() < end:
        line = s.readline()
        if line:
            print(line.decode(errors='replace').rstrip())
    s.close()
    print("\nDone.")
except Exception as e:
    print(f"ERROR: {e}")
