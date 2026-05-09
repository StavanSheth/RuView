"""Read serial logs from COM7 and COM10 simultaneously."""
import serial
import threading
import time
import sys
import os

# Force UTF-8 output
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

PORTS = ["COM7", "COM10"]
BAUD = 115200
READ_SECS = 20

lock = threading.Lock()
all_logs = {p: [] for p in PORTS}

def read_port(port):
    try:
        s = serial.Serial(port, BAUD, timeout=1)
        with lock:
            print(f"[{port}] OPENED OK")
        end = time.time() + READ_SECS
        while time.time() < end:
            line = s.readline()
            if line:
                text = line.decode(errors='replace').strip()
                all_logs[port].append(text)
                with lock:
                    print(f"[{port}] {text}")
        s.close()
        with lock:
            print(f"[{port}] Done reading.")
    except Exception as e:
        with lock:
            print(f"[{port}] ERROR: {e}")

threads = []
for port in PORTS:
    t = threading.Thread(target=read_port, args=(port,), daemon=True)
    threads.append(t)
    t.start()

print(f"Reading COM7 and COM10 for {READ_SECS}s...\n")
for t in threads:
    t.join()

print("\n=== SUMMARY ===")
for port, lines in all_logs.items():
    keywords = ["wifi", "connect", "ip", "udp", "csi", "ssid", "error", "fail", "ready", "softap", "got ip", "disconnect", "socket", "send"]
    key_lines = [l for l in lines if any(k in l.lower() for k in keywords)]
    print(f"\n[{port}] Total lines: {len(lines)}")
    print(f"[{port}] Key lines:")
    for l in (key_lines if key_lines else lines[-10:]):
        print(f"  {l}")
