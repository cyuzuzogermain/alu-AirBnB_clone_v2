#!/usr/bin/env bash
# Sets up the web servers for the deployment of web_static

# Install nginx if not already installed
apt-get -y update
apt-get -y install nginx

# Create required directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
ln -sfn /data/web_static/releases/test/ /data/web_static/current

# Change ownership ONLY if ubuntu user exists
if id "ubuntu" &>/dev/null; then
    chown -R ubuntu:ubuntu /data/
fi

# Configure nginx
cat > /etc/nginx/sites-available/default <<'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm;

    server_name _;

    location / {
        try_files $uri $uri/ =404;
    }

    location /hbnb_static {
        alias /data/web_static/current/;
    }
}
EOF

# Restart nginx
service nginx restart
