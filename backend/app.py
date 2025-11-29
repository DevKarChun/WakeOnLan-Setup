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
WOL_INTERFACE = os.getenv("WOL_INTERFACE", "ens4")  # Interface name for WOL (default: ens4)
STATUS_INTERFACE = os.getenv("STATUS_INTERFACE", "ens3")  # Interface name for status checks (default: ens3)
PORT = int(os.getenv("PORT", 13579))  # Default to 13579 if not set

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

def is_online():
    """
    Check if PC is online by pinging via the public network (192.168.0.0/24) using ens3.
    Uses PC_STATUS_IP (e.g., 192.168.0.153) for status check on public network.
    Falls back to PC_IP if PC_STATUS_IP is not configured.
    """
    # Use PC_STATUS_IP for status check (public network), fallback to PC_IP if not set
    status_ip = PC_STATUS_IP if PC_STATUS_IP else PC_IP
    if not status_ip:
        return False
    try:
        # Ping the PC's public network IP (192.168.0.153) for status check
        # Use -I flag to specify the interface (ens3) for status checks
        # This ensures ping goes out via the correct network interface
        result = subprocess.run(
            ["ping", "-c", "1", "-I", STATUS_INTERFACE, status_ip],
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

def send_wol_packet(mac_address, interface_name=None):
    """
    Send Wake-on-LAN magic packet via the specified network interface.
    
    Args:
        mac_address: MAC address of the target PC
        interface_name: Network interface name to bind to (e.g., 'ens4' for private link)
    """
    # Calculate broadcast address from PC_IP network (assuming /24 subnet)
    if PC_IP:
        # Extract network prefix and create broadcast address
        ip_parts = PC_IP.split('.')
        if len(ip_parts) == 4:
            broadcast_addr = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.255"
        else:
            broadcast_addr = "255.255.255.255"  # Fallback to global broadcast
    else:
        broadcast_addr = "255.255.255.255"  # Fallback to global broadcast
    
    # Use socket to bind to the specific interface for multi-homed systems
    # This ensures WOL packets go out via the correct interface (ens4)
    try:
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Bind to the specific interface using SO_BINDTODEVICE (Linux-specific)
        # This requires the interface name (e.g., 'ens4'), not the IP address
        if interface_name:
            try:
                # SO_BINDTODEVICE requires the interface name as bytes
                sock.setsockopt(socket.SOL_SOCKET, 25, interface_name.encode())  # 25 = SO_BINDTODEVICE
            except (OSError, AttributeError):
                # If SO_BINDTODEVICE is not available (e.g., on macOS), try binding to interface IP
                # This is a fallback for systems that don't support SO_BINDTODEVICE
                if BROADCAST:
                    sock.bind((BROADCAST, 0))
        
        # Convert MAC address to bytes
        mac_bytes = bytes.fromhex(mac_address.replace(':', '').replace('-', ''))
        
        # Create magic packet: 6 bytes of 0xFF + 16 repetitions of MAC address
        magic_packet = b'\xff' * 6 + mac_bytes * 16
        
        # Send to broadcast address on port 9
        sock.sendto(magic_packet, (broadcast_addr, 9))
        sock.close()
    except Exception as e:
        # Fallback to library method if socket binding fails
        # This will use the default route, which may not be correct for multi-homed systems
        try:
            send_magic_packet(mac_address, ip_address=broadcast_addr, port=9)
        except Exception:
            # If fallback also fails, raise the original exception
            raise e

@app.route("/start")
def start():
    if not PC_MAC:
        return jsonify({"action": "start", "result": "error", "message": "PC_MAC not configured"}), 400
    
    try:
        # Send WOL packet via ens4 (private link / 192.168.100.x network)
        # This ensures the magic packet is sent from the correct network interface
        send_wol_packet(PC_MAC, interface_name=WOL_INTERFACE)
        return jsonify({"action": "start", "result": "sent"})
    except Exception as e:
        return jsonify({"action": "start", "result": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
