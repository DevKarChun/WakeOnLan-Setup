const path = require('path');
const fs = require('fs');

// Read .env file manually (no external dependencies needed)
function loadEnv() {
  const envPath = path.join(__dirname, '.env');
  const env = {};
  if (fs.existsSync(envPath)) {
    const content = fs.readFileSync(envPath, 'utf8');
    content.split('\n').forEach(line => {
      const match = line.match(/^\s*([^#=]+)=(.*)$/);
      if (match) {
        env[match[1].trim()] = match[2].trim();
      }
    });
  }
  return env;
}

const envVars = loadEnv();

// Use shell script wrapper instead of direct Python interpreter
// This bypasses PM2's Python interpreter issues
const scriptPath = path.resolve(__dirname, 'start_backend.sh');

module.exports = {
  apps: [{
    name: 'pc-control-backend',
    script: scriptPath,
    interpreter: '/bin/bash',  // Use bash instead of Python directly
    interpreter_args: [],
    cwd: __dirname,
    exec_mode: 'fork',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    error_file: path.join(__dirname, 'logs', 'err.log'),
    out_file: path.join(__dirname, 'logs', 'out.log'),
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    min_uptime: '10s',
    max_restarts: 10,
    restart_delay: 4000,
    env: {
      FLASK_ENV: 'production',
      PORT: envVars.PORT || '13579',
      PC_MAC: envVars.PC_MAC || '',
      PC_IP: envVars.PC_IP || '',
      PC_STATUS_IP: envVars.PC_STATUS_IP || '',
      BROADCAST: envVars.BROADCAST || ''
    }
  }]
};
