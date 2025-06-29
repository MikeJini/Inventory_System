#!/bin/sh

# Write runtime env vars into a JS file
cat <<EOF > /usr/share/nginx/html/env-config.js
window.__ENV__ = {
  API_URL: "$VITE_API_URL",
  NODE_ENV: "$VITE_NODE_ENV"
};
EOF

# Start the actual Nginx server
exec "$@"