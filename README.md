# Hardened Linux Captive Portal (IoT / Jetson / RPi)

A lightweight, hardware-level Captive Portal solution for Linux devices where standard NetworkManager AP modes fail due to hardware/driver constraints. 

Built specifically to bypass driver locks on **NVIDIA Jetson** boards running Ubuntu 22.04, this architecture uses low-level daemons (`hostapd` + `dnsmasq`) to ensure a 100% reliable failover access point when the internet drops.

## Tech Stack
* **Python 3 / Flask**: Captive portal backend and hardware command execution.
* **Bash**: Initialization, monitoring, and state switching logic.
* **hostapd & dnsmasq**: Low-level Wi-Fi broadcasting and DNS routing.
* **HTML/JS**: Responsive, modern dark-themed setup UI.

## Features
* **Bypasses OS Conflicts**: Fully hijacks the Wi-Fi adapter from NetworkManager to prevent D-Bus crashes.
* **Hardware AP Lock**: Forces a stable 2.4GHz broadcast to bypass regional OS locks.
* **Auto-Recovery**: Switches back to client mode seamlessly after receiving credentials.
