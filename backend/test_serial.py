import serial, time
try:
    s = serial.Serial('COM4', 115200, timeout=1)
    s.dtr = False; s.rts = False; time.sleep(0.1); s.dtr = True; s.rts = True; time.sleep(0.1); s.dtr = False; s.rts = False
    print('Reading from COM4 for 10 seconds...')
    end = time.time() + 10
    while time.time() < end:
        line = s.readline()
        if line: print("COM4:", line.decode(errors='ignore').strip())
    s.close()
except Exception as e:
    print('COM4 Error:', e)

try:
    s = serial.Serial('COM8', 115200, timeout=1)
    print('Reading from COM8 for 4 seconds...')
    end = time.time() + 4
    while time.time() < end:
        line = s.readline()
        if line: print("COM8:", line.decode(errors='ignore').strip())
    s.close()
except Exception as e:
    print('COM8 Error:', e)
