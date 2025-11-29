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

module.exports = {
  apps: [{
    name: 'pc-control-frontend',
    script: 'npm',
    args: 'start',
    cwd: __dirname,
    env: {
      PORT: 3000,
      BROWSER: 'none',
      NODE_ENV: 'production',
      // Read API configuration from .env file
      REACT_APP_API_HOST: envVars.REACT_APP_API_HOST || 'localhost',
      REACT_APP_API_PORT: envVars.REACT_APP_API_PORT || '13579'
    },
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    error_file: path.join(__dirname, 'logs', 'err.log'),
    out_file: path.join(__dirname, 'logs', 'out.log'),
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    min_uptime: '10s',
    max_restarts: 10,
    restart_delay: 4000
  }]
};
