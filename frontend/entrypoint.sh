#!/bin/sh

# Write runtime env vars into a JS file
cat <<EOF > /usr/share/nginx/html/env-config.js
window.__ENV__ = {
  API_URL: "$VITE_FLASK_URL",
  NODE_ENV: "$VITE_FLASK_PORT"
};
EOF

# Start the actual Nginx server
exec "$@"