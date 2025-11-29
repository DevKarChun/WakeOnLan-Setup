# Server Deployment Configuration

## Quick Setup Guide

After pulling from git, configure the following on your server:

### Backend Configuration (`backend/.env`)

```env
PC_MAC=00:11:22:33:44:55
PC_IP=192.168.100.XXX
PC_STATUS_IP=192.168.0.153
BROADCAST=192.168.100.3
WOL_INTERFACE=ens4
STATUS_INTERFACE=ens3
PORT=13579
```

**Notes:**
- `PC_MAC`: The MAC address of your target PC's network interface
- `PC_IP`: The target PC's IP address on the internal network (`192.168.100.XXX`)
- `PC_STATUS_IP`: The target PC's IP address on the public network (`192.168.0.153`) for status checks
- `BROADCAST`: Use the server's internal network IP (`192.168.100.3`) as fallback for interface binding
- `WOL_INTERFACE`: Network interface name for sending WOL packets (e.g., `ens4`). Should be connected to internal network (192.168.100.x)
- `STATUS_INTERFACE`: Network interface name for status checks (e.g., `ens3`). Should be connected to public network (192.168.0.x)
- `PORT`: Backend API port (default: 13579)

**Finding Interface Names:**
```bash
ip addr show
# Look for interfaces matching your network IPs:
# - WOL_INTERFACE: Interface with IP on 192.168.100.x network
# - STATUS_INTERFACE: Interface with IP on 192.168.0.x network
```

### Frontend Configuration (`frontend/.env`)

```env
REACT_APP_API_HOST=192.168.0.231
REACT_APP_API_PORT=13579
```

**Notes:**
- `REACT_APP_API_HOST`: Use the server's public/internet-facing IP (`192.168.0.231`) for web access
- `REACT_APP_API_PORT`: Must match the `PORT` value in `backend/.env`

## Network Architecture

- **Public Network** (`192.168.0.0/24`):
  - Server Interface: `ens3` (STATUS_INTERFACE)
  - Server IP: `192.168.0.231` - Used for web access and frontend-backend communication
  - PC IP: `192.168.0.153` - Used for status checks
  
- **Internal Network** (`192.168.100.0/24`):
  - Server Interface: `ens4` (WOL_INTERFACE)
  - Server IP: `192.168.100.3` - Used for Wake-on-LAN packets
  - PC IP: `192.168.100.XXX` - Target PC on internal network

## PM2 Setup

1. **Backend:**
   ```bash
   cd backend
   chmod +x start_backend.sh
   pm2 start ecosystem.config.js
   ```

2. **Frontend:**
   ```bash
   cd frontend
   pm2 start ecosystem.config.js
   ```

3. **Verify:**
   ```bash
   pm2 list
   pm2 logs
   ```

## Files Updated

- `backend/app.py` - Reads PORT from .env, CORS enabled
- `backend/ecosystem.config.js` - Reads .env, uses shell wrapper
- `backend/start_backend.sh` - PM2 wrapper script (NEW)
- `frontend/src/App.js` - Uses REACT_APP_API_HOST and REACT_APP_API_PORT
- `frontend/ecosystem.config.js` - Reads .env for API configuration
- `README.md` - Complete documentation updated
