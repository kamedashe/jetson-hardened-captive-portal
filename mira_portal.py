import os, subprocess
from flask import Flask, jsonify, request, send_from_directory, redirect

app = Flask(__name__, static_folder="ui")

@app.route("/")
def index(): 
    return send_from_directory("ui", "index.html")

@app.errorhandler(404)
def redirect_to_portal(e): 
    return redirect("/")

@app.route("/<path:path>")
def static_files(path): 
    return send_from_directory("ui", path)

@app.route("/networks", methods=["GET"])
def get_nets():
    # Hardware-level network scan bypassing NetworkManager
    try:
        res = subprocess.check_output("iw dev wlP1p1s0 scan | grep SSID", shell=True).decode()
        nets = [{"ssid": l.split("SSID: ")[1].strip()} for l in res.split("\n") if "SSID: " in l and l.strip() != "SSID: "]
        # Remove duplicates
        unique_nets = [dict(t) for t in {tuple(d.items()) for d in nets}]
        return jsonify(unique_nets)
    except Exception as e: 
        return jsonify([])

@app.route("/connect", methods=["POST"])
def connect():
    d = request.json
    ssid, pw = d.get("ssid"), d.get("password")
    
    # Shut down daemons, return hardware to OS, and connect to new Wi-Fi
    cmd = f"systemctl stop hostapd dnsmasq && nmcli dev set wlP1p1s0 managed yes && sleep 3 && nmcli dev wifi connect '{ssid}' password '{pw}'"
    subprocess.Popen(cmd, shell=True)
    
    return jsonify({"status": "connecting"})

if __name__ == "__main__": 
    # Run on port 80 to intercept captive portal requests
    app.run(host="0.0.0.0", port=80)
