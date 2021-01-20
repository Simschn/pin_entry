# Python Timing attack against Arduino

Requirements:
pyserial                     3.5
Python                       3.9.1 

sigrok-cli                   0.7.1
Libraries and features:
- libsigrok 0.5.1/5:0:1 (rt: 0.5.2/5:1:1).
 - Libs:
  - glib 2.66.2 (rt: 2.66.4/6604:4)
  - libzip 1.7.3
  - libserialport 0.1.1/1:0:1 (rt: 0.1.1/1:0:1)
  - libusb-1.0 1.0.24.11584 API 0x01000107
  - hidapi 0.10.0
  - bluez 5.55
  - libftdi 1.4
  - Host: x86_64-pc-linux-gnu, little-endian.
  - SCPI backends: TCP, serial, USBTMC.
- libsigrokdecode 0.5.2/6:0:2 (rt: 0.5.3/6:1:2).
 - Libs:
  - glib 2.66.3 (rt: 2.66.4/6604:4)
  - Python 3.9.0 / 0x30900f0 (API 1013, ABI 3)
  - Host: x86_64-pc-linux-gnu, little-endian.

  Usage: 
  - connect logic analyser and arduino with flashed pin_entry.hex to your linux desktop
  - run ```python3 brute.py```
         
