import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(5)

print(f"Listening for ESP32 CSI packets on {UDP_IP}:{UDP_PORT}...")

count = 0
try:
    while count < 10:
        data, addr = sock.recvfrom(1024)
        print(f"Received {len(data)} bytes from {addr}")
        count += 1
except socket.timeout:
    print("Timeout! No packets received in 5 seconds.")
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()
