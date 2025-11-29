# PC Control Dashboard

A modern web application for remotely controlling your PC using Wake-on-LAN (WOL) technology. This project consists of a Flask backend API and a React frontend with a beautiful, modern UI.

## Features

- 🟢 **Status Monitoring**: Real-time PC online/offline status checking
- 🚀 **Wake-on-LAN**: Remotely start your PC from anywhere
- 🎨 **Modern UI**: Professional dark mode design with subtle effects
- 📱 **Responsive**: Works seamlessly on desktop and mobile devices

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (for backend)
- **Node.js 16+** and **npm** (for frontend)
- **wakeonlan** utility (install via package manager)

### Installing wakeonlan

**macOS:**
```bash
brew install wakeonlan
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install wakeonlan
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install wakeonlan
```

## Project Structure

```
WOL/
├── backend/          # Flask API server
│   ├── app.py        # Main Flask application
│   └── venv/         # Python virtual environment (gitignored)
├── frontend/         # React frontend application
│   ├── src/          # React source files
│   ├── public/       # Static assets
│   └── package.json  # Node dependencies
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd WOL
```

### 2. Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

4. Install Python dependencies:
```bash
pip install -r ../requirements.txt
```

5. Create a `.env` file in the `backend` directory:
```bash
touch .env
```

6. Add your configuration to `.env`:
```env
PC_MAC=00:11:22:33:44:55
PC_IP=192.168.100.1
PC_STATUS_IP=192.168.0.153
BROADCAST=192.168.100.3
WOL_INTERFACE=ens4
STATUS_INTERFACE=ens3
PORT=13579
```

**Configuration Details:**
- `PC_MAC`: The MAC address of your target PC's network interface
- `PC_IP`: The IP address of your target PC on the **internal network** (e.g., `192.168.100.1`). Used for WOL packets.
- `PC_STATUS_IP`: The IP address of your target PC on the **public network** (e.g., `192.168.0.153`). Used for status checks (ping). If not set, falls back to `PC_IP`.
- `BROADCAST`: The internal network IP address of the server (e.g., `192.168.100.3`). Used as fallback for interface binding if interface names are not available.
- `WOL_INTERFACE`: The network interface name to use for sending WOL packets (e.g., `ens4`). Defaults to `ens4` if not set. **Important:** This should be the interface connected to the internal/private network (192.168.100.x).
- `STATUS_INTERFACE`: The network interface name to use for status checks (e.g., `ens3`). Defaults to `ens3` if not set. **Important:** This should be the interface connected to the public/LAN network (192.168.0.x).
- `PORT`: The port number for the backend API server (default: 13579). Change this if port 13579 is already in use.

**Finding Your Network Interface Names:**

To find the correct interface names on Linux, use one of these commands:

```bash
# List all network interfaces with their IP addresses
ip addr show

# Or use ifconfig (if installed)
ifconfig

# Or list interfaces with routing info
ip route show
```

Look for interfaces that match your network configuration:
- **WOL Interface** (`WOL_INTERFACE`): Should be the interface with an IP on your internal/private network (e.g., `192.168.100.x`). Common names: `ens4`, `eth1`, `enp3s0`, etc.
- **Status Interface** (`STATUS_INTERFACE`): Should be the interface with an IP on your public/LAN network (e.g., `192.168.0.x`). Common names: `ens3`, `eth0`, `enp2s0`, etc.

**Example output:**
```
1: lo: <LOOPBACK,UP,LOWER_UP> ...
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    inet 192.168.0.231/24 ...  # This is your STATUS_INTERFACE
3: ens4: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    inet 192.168.100.3/24 ...   # This is your WOL_INTERFACE
```

**Network Configuration Notes:**
- **Dual Network Setup:**
  - **Internal Network** (`192.168.100.0/24`): Used for WOL packets
    - Server Interface: `ens4` (or your `WOL_INTERFACE`)
    - Server IP: `192.168.100.3`
    - PC: `192.168.100.1` (wired connection)
  - **Public Network** (`192.168.0.0/24`): Used for status checks and web access
    - Server Interface: `ens3` (or your `STATUS_INTERFACE`)
    - Server IP: `192.168.0.231` (use in frontend `.env` for `REACT_APP_API_HOST`)
    - PC: `192.168.0.153` (use for `PC_STATUS_IP`)

### 3. Frontend Setup

1. Navigate to the frontend directory:
```bash
cd ../frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Create a `.env` file in the `frontend` directory:
```bash
touch .env
```

4. Add your configuration to `.env`:
```env
REACT_APP_API_HOST=192.168.0.231
REACT_APP_API_PORT=13579
```

**Configuration Details:**
- `REACT_APP_API_HOST`: The public/internet-facing IP address of the backend server (e.g., `192.168.0.231`). Use `localhost` only if frontend and backend are on the same machine and accessed locally. For internet access, use the server's public IP address. Default is `localhost`.
- `REACT_APP_API_PORT`: The port number where the backend API is running. This should match the `PORT` value in `backend/.env`. Default is `13579`.
- **Important:** The variable names must start with `REACT_APP_` prefix. React only exposes environment variables that start with `REACT_APP_` to the browser.
- **Note:** After changing `.env`, you must restart the React development server for changes to take effect.

**Network Configuration Notes:**
- If your server has multiple network interfaces:
  - Use the **public/internet-facing IP** (e.g., `192.168.0.231`) for `REACT_APP_API_HOST` so users can access the website from the internet
  - The backend uses the **internal network IP** (e.g., `192.168.100.3`) for `BROADCAST` in `backend/.env` to send WOL packets

## Running the Application

You have two options for running the application:

- **Option 1: Manual Start** - Run backend and frontend manually in separate terminals (good for development)
- **Option 2: Process Management with PM2** - Use PM2 to manage both processes (recommended for production)

---

### Option 1: Manual Start

This method runs the backend and frontend in separate terminal windows. This is ideal for development and debugging.

#### Start Backend Server

1. Open a terminal and navigate to the backend directory:
```bash
cd backend
```

2. Activate the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate      # Windows
```

3. Start the Flask server:
```bash
python app.py
```

The backend will start on `http://localhost:13579` (or the port specified in your `.env` file)

#### Start Frontend Server

1. Open a **new terminal window/tab** and navigate to the frontend directory:
```bash
cd frontend
```

2. Start the React development server:
```bash
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

**Note:** Keep both terminal windows open while using the application. To stop the servers, press `Ctrl+C` in each terminal.

---

### Option 2: Process Management with PM2

PM2 is a process manager that provides automatic restarts, logging, and process monitoring. This is the recommended method for production use.

Follow these steps in order to set up and run both backend and frontend using PM2.

#### Step 1: Install PM2

First, install PM2 globally on your system:

**macOS/Linux:**
```bash
npm install -g pm2
```

**Windows:**
```bash
npm install -g pm2-windows-startup
pm2-startup install
```

Verify PM2 installation:
```bash
pm2 --version
```

You should see a version number (e.g., `5.3.0`).

#### Step 2: Verify Backend Setup

Before starting with PM2, ensure your backend is properly configured:

1. **Verify virtual environment exists:**
```bash
cd backend
ls venv/bin/activate  # macOS/Linux
# or
ls venv\Scripts\activate  # Windows
```

If the virtual environment doesn't exist, create it:
```bash
python3 -m venv venv
```

2. **Verify dependencies are installed:**
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate      # Windows

pip list | grep Flask
```

You should see Flask and related packages. If not, install them:
```bash
pip install -r ../requirements.txt
```

3. **Verify .env file exists:**
```bash
ls .env
```

If `.env` doesn't exist, create it:
```bash
touch .env
```

Then add your configuration:
```env
PC_MAC=00:11:22:33:44:55
PC_IP=192.168.100.1
PC_STATUS_IP=192.168.0.153
BROADCAST=192.168.100.3
WOL_INTERFACE=ens4
STATUS_INTERFACE=ens3
PORT=13579
```

**Note:** Replace the values above with your actual PC configuration. Make sure to set `WOL_INTERFACE` and `STATUS_INTERFACE` to match your network interface names (use `ip addr show` to find them).

4. **Verify PM2 config file exists:**
```bash
ls ecosystem.config.js
```

The `ecosystem.config.js` file should already exist in the `backend/` directory. If it doesn't, you'll need to create it (see troubleshooting section).

#### Step 3: Start Backend with PM2

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Start the backend service:**
```bash
pm2 start ecosystem.config.js
```

3. **Verify backend is running:**
```bash
pm2 list
```

You should see `pc-control-backend` in the list with status `online`.

4. **Check backend logs:**
```bash
pm2 logs pc-control-backend
```

You should see Flask startup messages. Press `Ctrl+C` to exit the log view.

5. **Verify backend is responding:**
```bash
curl http://localhost:13579/status
# Or if you changed PORT in .env, use that port instead
```

You should receive a JSON response with the PC status.

#### Step 4: Verify Frontend Setup

Before starting the frontend with PM2, ensure it's properly configured:

1. **Navigate to frontend directory:**
```bash
cd ../frontend
```

2. **Verify dependencies are installed:**
```bash
ls node_modules
```

If `node_modules` doesn't exist or is empty, install dependencies:
```bash
npm install
```

3. **Verify .env file exists:**
```bash
ls .env
```

If `.env` doesn't exist, create it:
```bash
touch .env
```

Then add your configuration:
```env
REACT_APP_API_HOST=192.168.0.231
REACT_APP_API_PORT=13579
```

**Important:** 
- `REACT_APP_API_HOST`: Use `localhost` if frontend and backend are on the same machine, or use the server's IP address (e.g., `192.168.1.100`) if accessing from a different machine.
- `REACT_APP_API_PORT`: The value must match the `PORT` value in `backend/.env`. If you changed the backend port, update this value to match.

4. **Verify PM2 config file exists:**
```bash
ls ecosystem.config.js
```

The `ecosystem.config.js` file should already exist in the `frontend/` directory. If it doesn't, you'll need to create it (see troubleshooting section).

#### Step 5: Start Frontend with PM2

1. **Ensure you're in the frontend directory:**
```bash
cd frontend
```

2. **Start the frontend service:**
```bash
pm2 start ecosystem.config.js
```

3. **Verify frontend is running:**
```bash
pm2 list
```

You should see both `pc-control-backend` and `pc-control-frontend` in the list with status `online`.

4. **Check frontend logs:**
```bash
pm2 logs pc-control-frontend
```

You should see React compilation messages. Press `Ctrl+C` to exit the log view.

5. **Verify frontend is accessible:**
Open your browser and navigate to:
```
http://localhost:3000
```

You should see the PC Control Dashboard.

#### Step 6: Verify Both Services

1. **View all PM2 processes:**
```bash
pm2 list
```

You should see:
- `pc-control-backend` - status: `online`
- `pc-control-frontend` - status: `online`

2. **View all logs:**
```bash
pm2 logs
```

This shows logs from both services. Press `Ctrl+C` to exit.

3. **Monitor processes:**
```bash
pm2 monit
```

This opens an interactive monitor showing CPU and memory usage. Press `Ctrl+C` to exit.

**Congratulations!** Both services are now running with PM2. The application is ready to use.

#### Troubleshooting PM2 Errors

If you see processes with empty status, "errored" status, or high restart counts (↺) when running `pm2 list`, follow these steps:

1. **Check the error logs immediately (THIS IS THE MOST IMPORTANT STEP):**
```bash
# View recent logs (most important - shows the actual error)
pm2 logs pc-control-backend --lines 100 --err    # Backend errors only
pm2 logs pc-control-frontend --lines 100 --err   # Frontend errors only
pm2 logs --lines 100                              # All logs (errors and output)

# Or check the log files directly
cat backend/logs/err.log
cat frontend/logs/err.log
cat backend/logs/out.log
cat frontend/logs/out.log
```

2. **If processes show empty status or high restart counts:**
   - Empty status usually means the process crashed immediately
   - High restart count (↺) means PM2 is trying to restart but failing
   - **First step:** Check the logs above to see the actual error
   - **Second step:** Stop and delete all processes, then restart fresh:
   ```bash
   pm2 stop all
   pm2 delete all
   ```

3. **If backend starts then crashes (restart count increasing):**
   - This usually means a runtime error. Check logs first!
   - Common causes:
     - Missing `.env` file or incorrect environment variables
     - Port already in use (another process on port 13579)
     - Missing Python dependencies
     - Python syntax error in app.py

3. **Stop and delete errored processes:**
```bash
pm2 stop all
pm2 delete all
```

3. **For Backend Errors (especially if it starts then crashes):**

   **First, check what the actual error is:**
   ```bash
   pm2 logs pc-control-backend --lines 50 --err
   # OR
   tail -50 backend/logs/err.log
   ```

   **Then verify each component:**

   a. **Check .env file exists and has correct values:**
   ```bash
   cd backend
   ls -la .env
   cat .env
   # Should show PC_MAC, PC_IP, BROADCAST, WOL_INTERFACE, and STATUS_INTERFACE variables
   ```

   b. **Check if port 13579 is already in use:**
   ```bash
   lsof -i :13579
   # or
   netstat -tulpn | grep 13579
   # If something is using the port, kill it or change the port in app.py
   ```

   c. **Test if app.py runs manually (this will show the actual error):**
   ```bash
   cd backend
   source venv/bin/activate
   python app.py
   # Watch for any error messages - this is what PM2 is seeing
   # Press Ctrl+C to stop after testing
   ```

   d. **Verify Python interpreter:**
   ```bash
   cd backend
   ls -la venv/bin/python
   ./venv/bin/python --version
   ```

   e. **Verify all dependencies are installed:**
   ```bash
   cd backend
   source venv/bin/activate
   pip list | grep -E "(Flask|flask-cors|wakeonlan|python-dotenv)"
   # Should show all packages installed
   ```

4. **For Frontend Errors:**
   - Verify npm: `which npm && npm --version`
   - Test manually: `cd frontend && npm start`
   - Check node_modules: `cd frontend && ls node_modules`
   - Reinstall if needed: `cd frontend && rm -rf node_modules && npm install`

5. **Clean restart with PM2 (recommended if processes keep crashing):**
```bash
# Stop and delete all processes first
pm2 stop all
pm2 delete all

# Verify they're gone
pm2 list

# Start backend fresh
cd backend
pm2 start ecosystem.config.js

# Wait a moment, check if it's running
sleep 2
pm2 list
pm2 logs pc-control-backend --lines 20

# If backend is online, start frontend
cd ../frontend
pm2 start ecosystem.config.js

# Check both
pm2 list
pm2 logs --lines 20
```

6. **If issues persist, check the log files directly:**
```bash
# Check error logs
cat backend/logs/err.log
cat frontend/logs/err.log

# Check output logs (sometimes errors are here)
cat backend/logs/out.log
cat frontend/logs/out.log

# Check PM2's own logs
pm2 logs --lines 50 --nostream
```

7. **Common issues and fixes:**

   **Backend keeps crashing or shows empty status:**
   - Missing `.env` file: `cd backend && ls -la .env`
   - Wrong Python path: `cd backend && ls -la venv/bin/python`
   - Port already in use: `lsof -i :13579` or check your `.env` PORT value
   - Missing dependencies: `cd backend && source venv/bin/activate && pip list`
   - PM2 internal error (SyntaxError in PM2 files): This is a PM2 installation issue, not your code
     - Backend might actually be working (check logs for "200" responses)
     - Try: `pm2 delete pc-control-backend && cd backend && pm2 start ecosystem.config.js`
     - Or reinstall PM2: `npm uninstall -g pm2 && npm install -g pm2`

   **Frontend keeps crashing or restarting repeatedly:**
   - Missing `.env` file: `cd frontend && ls -la .env`
   - Missing node_modules: `cd frontend && ls node_modules`
   - Port 3000 in use: `lsof -i :3000`
   - npm not found: `which npm`
   - react-scripts not found: `ls node_modules/.bin/react-scripts`
   - Check error logs: `cat frontend/logs/err.log | tail -50`
   - Test manually: `cd frontend && npm start` (this will show the actual error)
   - PM2 environment variables not loaded: React needs `REACT_APP_API_PORT` in environment
     - Check: `pm2 env 2` (where 2 is the process ID)
     - Restart with env: `pm2 restart pc-control-frontend --update-env`

#### PM2 Management Commands

**View all processes:**
```bash
pm2 list
```

**View logs:**
```bash
pm2 logs pc-control-backend    # Backend logs only
pm2 logs pc-control-frontend   # Frontend logs only
pm2 logs                        # All logs
```

**Stop processes:**
```bash
pm2 stop pc-control-backend     # Stop backend only
pm2 stop pc-control-frontend    # Stop frontend only
pm2 stop all                    # Stop all processes
```

**Restart processes:**
```bash
pm2 restart pc-control-backend  # Restart backend only
pm2 restart pc-control-frontend # Restart frontend only
pm2 restart all                 # Restart all processes
```

**Delete processes:**
```bash
pm2 delete pc-control-backend   # Delete backend from PM2
pm2 delete pc-control-frontend  # Delete frontend from PM2
pm2 delete all                  # Delete all processes
```

**Monitor processes:**
```bash
pm2 monit
```

**View process information:**
```bash
pm2 info pc-control-backend
pm2 info pc-control-frontend
```

**Save PM2 process list (for auto-restart on reboot):**
```bash
pm2 save
pm2 startup                     # Generate startup script
```

**Note:** After running `pm2 startup`, follow the instructions provided to enable automatic startup on system boot.

---

## Usage

1. **Check Status**: The dashboard automatically checks your PC status every 5 seconds
2. **Start PC**: Click the "Start PC" button to send a Wake-on-LAN magic packet

## API Endpoints

The backend provides the following REST API endpoints:

- `GET /status` - Get the current online/offline status of the PC
- `GET /start` - Send a Wake-on-LAN packet to start the PC

## Troubleshooting

### Backend Issues

**Port already in use:**
- Change the `PORT` value in `backend/.env` file to a different port (e.g., `PORT=8080`)
- Change the `REACT_APP_API_PORT` value in `frontend/.env` file to match (e.g., `REACT_APP_API_PORT=8080`)
- Restart both backend and frontend servers for changes to take effect

**Frontend cannot connect to backend (Connection Error):**
- If frontend and backend are on different machines, set `REACT_APP_API_HOST` in `frontend/.env` to the backend server's IP address (e.g., `REACT_APP_API_HOST=192.168.1.100`)
- Ensure `REACT_APP_API_PORT` matches the backend `PORT` in `backend/.env`
- Restart the frontend after updating `.env`: `pm2 restart pc-control-frontend --update-env`
- If using PM2: 
  ```bash
  pm2 restart pc-control-backend
  pm2 restart pc-control-frontend
  ```
- **Note:** After changing the frontend `.env` file, you must restart the React development server for changes to take effect (React reads environment variables at build/start time)

**Environment variables not loading:**
- Ensure `.env` file is in the `backend` directory
- Check that variable names match exactly (case-sensitive)

**wakeonlan command not found:**
- Install wakeonlan using your system's package manager (see Prerequisites)

**PM2 backend not starting or showing "errored" status:**

1. **Check PM2 logs for detailed error messages:**
```bash
pm2 logs pc-control-backend --lines 50
```

2. **Verify Python interpreter path:**
```bash
cd backend
ls -la venv/bin/python
# Should show the Python executable exists
```

3. **Test Python interpreter manually:**
```bash
cd backend
./venv/bin/python --version
# Should show Python version
```

4. **Test if app.py runs manually:**
```bash
cd backend
source venv/bin/activate
python app.py
# Should start Flask server without errors
```

5. **Check if .env file exists and is readable:**
```bash
cd backend
ls -la .env
cat .env
# Verify the file exists and has correct content
```

6. **Verify all dependencies are installed:**
```bash
cd backend
source venv/bin/activate
pip list | grep -E "(Flask|flask-cors|wakeonlan|python-dotenv)"
```

7. **Delete and restart PM2 process:**
```bash
pm2 delete pc-control-backend
cd backend
pm2 start ecosystem.config.js
pm2 logs pc-control-backend
```

8. **If interpreter path is wrong, update ecosystem.config.js:**
   - Find your Python path: `which python3` or `cd backend && which venv/bin/python`
   - Update `interpreter` field in `backend/ecosystem.config.js` with absolute path if needed

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running and accessible
- If frontend and backend are on different machines, set `REACT_APP_API_HOST` in `frontend/.env` to the backend server's IP address
- Verify `REACT_APP_API_PORT` in `frontend/.env` matches the `PORT` in `backend/.env`
- Check CORS settings in `backend/app.py` (should have `CORS(app)` enabled)
- Verify the API URL is correctly built from environment variables in `frontend/src/App.js`

**Port 3000 already in use:**
- React will prompt you to use another port
- Or kill the process using port 3000: `lsof -ti:3000 | xargs kill` (macOS/Linux)
- Or use PM2 to manage the process

**PM2 frontend not starting or showing "errored" status:**

1. **Check PM2 logs for detailed error messages:**
```bash
pm2 logs pc-control-frontend --lines 50
```

2. **"react-scripts: not found" error:**
   This means dependencies are not installed properly. Fix it:
   ```bash
   cd frontend
   # Fix permissions first (if you used sudo npm install)
   sudo chown -R $USER:$USER node_modules package-lock.json package.json .env
   # Remove old dependencies
   sudo rm -rf node_modules package-lock.json
   # Reinstall dependencies (DO NOT use sudo for npm install)
   npm install
   # Wait for installation to complete (this takes several minutes - should install 1000+ packages)
   # Verify react-scripts is installed
   ls node_modules/.bin/react-scripts
   # Should show the react-scripts executable
   ```

   **Important:** 
   - Never use `sudo npm install` as it causes permission issues
   - A proper npm install should install 1000+ packages, not just 50-60
   - If you see "added 54 packages" or similar low numbers, the install didn't work properly
   - Check package.json has `react-scripts` listed: `cat package.json | grep react-scripts`
   
   **If npm install keeps failing or only installs 50-60 packages:**
   
   **Check if react-scripts version is wrong:**
   ```bash
   npm list react-scripts
   # If it shows react-scripts@0.0.0, the package-lock.json is corrupted
   ```
   
   **Fix corrupted package-lock.json:**
   ```bash
   cd frontend
   # Remove everything (package-lock.json is corrupted)
   sudo rm -rf node_modules package-lock.json
   # Clear npm cache
   npm cache clean --force
   # Fix ownership
   sudo chown -R $USER:$USER .
   # Verify package.json has correct react-scripts version
   cat package.json | grep react-scripts
   # Should show: "react-scripts": "5.0.1"
   # If it shows "0.0.0", fix package.json first
   # Install fresh (DO NOT use sudo)
   npm install
   # Should see "added 1000+ packages" or similar, NOT just 50-60
   # Verify react-scripts version is correct
   npm list react-scripts
   # Should show react-scripts@5.0.1, NOT 0.0.0
   # Verify react-scripts executable exists
   ls node_modules/.bin/react-scripts
   ```

   **If react-scripts still shows 0.0.0 after reinstall:**
   
   **Check package-lock.json:**
   ```bash
   cd frontend
   grep -A 2 '"react-scripts"' package-lock.json
   # If it shows "0.0.0", the lock file is corrupted
   ```
   
   **Fix corrupted package-lock.json or package.json:**
   ```bash
   cd frontend
   # Remove the corrupted lock file
   sudo rm -f package-lock.json
   # Remove node_modules
   sudo rm -rf node_modules
   # Fix ownership
   sudo chown -R $USER:$USER .
   # Check package.json version
   cat package.json | grep react-scripts
   # Should show: "react-scripts": "5.0.1"
   # If it shows "^0.0.0", fix package.json first:
   sed -i 's/"react-scripts": "\^0\.0\.0"/"react-scripts": "5.0.1"/' package.json
   # OR manually edit package.json line 13 to: "react-scripts": "5.0.1",
   # Verify it's fixed
   cat package.json | grep react-scripts
   # Should now show: "react-scripts": "5.0.1"
   # Install fresh (this will create new package-lock.json)
   npm install
   # Should see "added 1000+ packages" and react-scripts@5.0.1
   # This takes several minutes - wait for completion
   # Verify
   npm list react-scripts
   # Should show react-scripts@5.0.1, NOT 0.0.0
   ls node_modules/.bin/react-scripts
   # Should show the executable
   ```

3. **Verify .env file has correct variable names:**
   ```bash
   cd frontend
   cat .env
   ```
   Should show:
   ```
   REACT_APP_API_HOST=192.168.0.231
   REACT_APP_API_PORT=16742
   ```
   **NOT** `PORT=16742` (that's wrong!)
   
   If wrong or permission denied, fix it:
   ```bash
   cd frontend
   # Fix permissions if needed
   sudo chown $USER:$USER .env 2>/dev/null || true
   # Create/update .env file
   # Replace 192.168.0.231 with your server's public IP address
   # Replace 16742 with your actual backend port
   cat > .env << 'EOF'
   REACT_APP_API_HOST=192.168.0.231
   REACT_APP_API_PORT=16742
   EOF
   # Verify it worked
   cat .env
   ```
   
   **If you get "Permission denied" error:**
   - The .env file might be owned by root (if created with sudo)
   - Fix ownership: `sudo chown $USER:$USER .env`
   - Then edit normally using the `cat > .env` method above

4. **Verify npm is available:**
```bash
which npm
npm --version
```

5. **Test if npm start works manually:**
```bash
cd frontend
npm start
# Should start React dev server without errors
# Press Ctrl+C to stop after testing
```

6. **Verify node_modules exists:**
```bash
cd frontend
ls -la node_modules
# Should show node_modules directory with many packages
```

7. **Check if port 3000 is available:**
```bash
lsof -i :3000  # macOS/Linux
# or
netstat -ano | findstr :3000  # Windows
```

8. **Delete and restart PM2 process:**
```bash
pm2 delete pc-control-frontend
cd frontend
pm2 start ecosystem.config.js
pm2 logs pc-control-frontend
```

9. **If npm path is wrong, update ecosystem.config.js:**
   - Find npm path: `which npm`
   - Update `script` field in `frontend/ecosystem.config.js` with absolute path if needed

### Network Issues

**Wake-on-LAN not working:**
- Ensure your PC's BIOS has Wake-on-LAN enabled
- Verify the MAC address is correct
- Check that your router supports Wake-on-LAN broadcasts
- Ensure the PC is connected to the same network segment
- **For multi-homed systems:** Verify that `WOL_INTERFACE` is set to the correct interface name (e.g., `ens4` for the internal/private network)
  - Check your interface names: `ip addr show` or `ifconfig`
  - Ensure `WOL_INTERFACE` matches the interface connected to the internal network (192.168.100.x)
  - The interface should have an IP address on the same network as `PC_IP`

**Status checks not working:**
- **For multi-homed systems:** Verify that `STATUS_INTERFACE` is set to the correct interface name (e.g., `ens3` for the public/LAN network)
  - Check your interface names: `ip addr show` or `ifconfig`
  - Ensure `STATUS_INTERFACE` matches the interface connected to the public network (192.168.0.x)
  - The interface should have an IP address on the same network as `PC_STATUS_IP`
- Verify that `PC_STATUS_IP` is correct and reachable from the server
- Test connectivity manually: `ping -I <STATUS_INTERFACE> <PC_STATUS_IP>`

**SSH commands failing:**
- Ensure SSH is configured and accessible
- Verify SSH key authentication is set up
- Check that the PC_IP is correct and reachable

### Git Issues

**"fatal: detected dubious ownership in repository" error:**

This error occurs when Git detects that the repository is owned by a different user than the one running Git commands. This is a security feature.

**Solution:**

Add the repository directory to Git's safe directory list:

```bash
git config --global --add safe.directory /home/ubuntu/wol/WakeOnLan-Setup
```

Replace `/home/ubuntu/wol/WakeOnLan-Setup` with your actual repository path.

**To find your repository path:**
```bash
pwd
# This will show your current directory path
```

**Alternative: Add current directory as safe:**
```bash
git config --global --add safe.directory "$(pwd)"
```

**Verify the fix:**
```bash
git status
# Should now work without errors
```

**Note:** This adds the directory to your global Git configuration. If you want to add multiple directories, run the command for each one.

## Development

### Backend Development

The Flask backend uses:
- Flask for the web framework
- flask-cors for CORS support
- python-dotenv for environment variable management
- wakeonlan for sending magic packets

### Frontend Development

The React frontend uses:
- React 19.2.0
- Axios for API calls
- Modern CSS with professional dark mode design

## Security Notes

⚠️ **Important Security Considerations:**

- This application should only be used on trusted networks
- Consider adding authentication for production use
- The SSH commands assume passwordless SSH access
- Environment variables contain sensitive information - never commit `.env` files
- When using PM2, ensure proper file permissions on configuration files

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
