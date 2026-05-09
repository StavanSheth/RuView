# RuView Easy Quickstart

Because your ESP32 hardware is now successfully permanently flashed and provisioned with your hotspot credentials in its non-volatile storage (NVS), **you do not need to repeat any Python scripts or flashing commands ever again!**

## How to launch RuView moving forward:

1. **Turn on Mobile Hotspot:** In your Windows settings, switch on your Mobile Hotspot (Name: `STAVAN-DESKSTOP 2500`).
2. **Power the hardware:** Plug your two ESP32 units into any USB power source (wall adapter, laptop, or power bank). They will instantly connect to your hotspot.
3. **Double-click:** Go to `C:\Projects\RuView` and double click the `Launch-RuView.bat` file! 

That's it! The batch file will automatically boot up the Rust pipeline and launch your web browser straight to the dashboard. 

## Troubleshooting
If you move to a new house or change your hotspot name, you will need to re-provision the Wi-Fi credentials to the ESP32s over a serial cable. To do this, open PowerShell, connect your ESP32, and run:
```powershell
python firmware/esp32-csi-node/provision.py --port COM4 --ssid "Your_New_Network" --password "Your_Password" --target-ip 192.168.137.1 --node-id 1
```
