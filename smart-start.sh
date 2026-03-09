#!/bin/bash
# Autonomous Captive Portal Trigger for Jetson/Ubuntu
IFACE="wlP1p1s0"

# 1. Allow NetworkManager to check connection
nmcli dev set $IFACE managed yes
sleep 3

# 2. Check if internet is available
if [ "$(nmcli -t -f CONNECTIVITY general)" = "full" ]; then
    echo "Internet is UP. Shutting down portal daemons."
    systemctl stop hostapd dnsmasq 2>/dev/null
    exit 0
fi

echo "Internet is DOWN. Initializing Captive Portal..."

# 3. Take hardware control away from NetworkManager
nmcli dev set $IFACE managed no
sleep 2

# 4. Set static IP for the router
ip addr flush dev $IFACE
ip addr add 10.42.0.1/24 dev $IFACE
ip link set $IFACE up

# 5. Start low-level AP daemons
systemctl restart dnsmasq
systemctl restart hostapd

# 6. Launch the Python Web Backend
exec python3 /opt/wifi-connect/mira_portal.py
