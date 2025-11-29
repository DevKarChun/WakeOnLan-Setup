from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import os
import socket
from dotenv import load_dotenv
from wakeonlan import send_magic_packet

# Load environment variables
load_dotenv()

PC_MAC = os.getenv("PC_MAC")
PC_IP = os.getenv("PC_IP")  # Internal network IP for WOL (e.g., 192.168.100.1)
PC_STATUS_IP = os.getenv("PC_STATUS_IP")  # Public network IP for status check (e.g., 192.168.0.153)
BROADCAST = os.getenv("BROADCAST")  # Internal network IP for WOL (e.g., 192.168.100.3)
PORT = int(os.getenv("PORT", 13579))  # Default to 13579 if not set

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

def is_online():
    """
    Check if PC is online by pinging via the public network (192.168.0.0/24).
    Uses PC_STATUS_IP (e.g., 192.168.0.153) for status check on public network.
    Falls back to PC_IP if PC_STATUS_IP is not configured.
    """
    # Use PC_STATUS_IP for status check (public network), fallback to PC_IP if not set
    status_ip = PC_STATUS_IP if PC_STATUS_IP else PC_IP
    if not status_ip:
        return False
    try:
        # Ping the PC's public network IP (192.168.0.153) for status check
        # This uses the public network (192.168.0.0/24) for status monitoring
        result = subprocess.run(
            ["ping", "-c", "1", status_ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False

@app.route("/status")
def status():
    # Status check uses PC_STATUS_IP (public network) if available, otherwise PC_IP
    status_ip = PC_STATUS_IP if PC_STATUS_IP else PC_IP
    if not status_ip:
        return jsonify({"online": False, "error": "PC_IP or PC_STATUS_IP not configured"}), 200
    return jsonify({"online": is_online()})

def send_wol_packet(mac_address, interface_ip=None, target_ip=None):
    """
    Send Wake-on-LAN magic packet.
    
    Args:
        mac_address: MAC address of the target PC
        interface_ip: IP address of the interface to bind to (for multi-homed systems)
        target_ip: Target IP/broadcast address (defaults to broadcast on target network)
    """
    # Calculate broadcast address from PC_IP network (assuming /24 subnet)
    if target_ip:
        broadcast_addr = target_ip
    elif PC_IP:
        # Extract network prefix and create broadcast address
        ip_parts = PC_IP.split('.')
        if len(ip_parts) == 4:
            broadcast_addr = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.255"
        else:
            broadcast_addr = "255.255.255.255"  # Fallback to global broadcast
    else:
        broadcast_addr = "255.255.255.255"  # Fallback to global broadcast
    
    # If interface_ip is specified, we need to bind to that interface
    # The Python wakeonlan library doesn't support interface binding directly,
    # so we'll use socket to create a bound socket and send the packet
    if interface_ip:
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            # Bind to the specific interface
            sock.bind((interface_ip, 0))
            
            # Convert MAC address to bytes
            mac_bytes = bytes.fromhex(mac_address.replace(':', '').replace('-', ''))
            
            # Create magic packet: 6 bytes of 0xFF + 16 repetitions of MAC address
            magic_packet = b'\xff' * 6 + mac_bytes * 16
            
            # Send to broadcast address on port 9
            sock.sendto(magic_packet, (broadcast_addr, 9))
            sock.close()
        except Exception as e:
            # Fallback to library method if socket binding fails
            send_magic_packet(mac_address, ip_address=broadcast_addr, port=9)
    else:
        # No interface binding needed, use library directly
        send_magic_packet(mac_address, ip_address=broadcast_addr, port=9)

@app.route("/start")
def start():
    if not PC_MAC:
        return jsonify({"action": "start", "result": "error", "message": "PC_MAC not configured"}), 400
    
    try:
        # Send WOL packet using the interface specified in BROADCAST (if set)
        # BROADCAST contains the server's IP on the internal network (e.g., 192.168.100.3)
        # This ensures the packet is sent from the correct network interface
        send_wol_packet(PC_MAC, interface_ip=BROADCAST)
        return jsonify({"action": "start", "result": "sent"})
    except Exception as e:
        return jsonify({"action": "start", "result": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
