# Server Deployment Configuration

## Quick Setup Guide

After pulling from git, configure the following on your server:

### Backend Configuration (`backend/.env`)

```env
PC_MAC=00:11:22:33:44:55
PC_IP=192.168.100.XXX
BROADCAST=192.168.100.3
PORT=13579
```

**Notes:**
- `BROADCAST`: Use the server's internal network IP (`192.168.100.3`) for Wake-on-LAN packets
- `PC_IP`: The target PC's IP address on the internal network (`192.168.100.XXX`)
- `PORT`: Backend API port (default: 13579)

### Frontend Configuration (`frontend/.env`)

```env
REACT_APP_API_HOST=192.168.0.231
REACT_APP_API_PORT=13579
```

**Notes:**
- `REACT_APP_API_HOST`: Use the server's public/internet-facing IP (`192.168.0.231`) for web access
- `REACT_APP_API_PORT`: Must match the `PORT` value in `backend/.env`

## Network Architecture

- **Public IP** (`192.168.0.231`): Used for web access and frontend-backend communication
- **Internal IP** (`192.168.100.3`): Used for Wake-on-LAN packets to target PC

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
