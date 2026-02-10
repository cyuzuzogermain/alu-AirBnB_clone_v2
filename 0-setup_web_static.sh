#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# 1. Install Nginx if not already installed
sudo apt-get update -y
sudo apt-get install -y nginx

# 2. Create directory structure
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# 3. Create a fake HTML file to test the configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# 4. Create/Recreate symbolic link
# -s: symbolic, -f: force (removes existing destination files)
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# 5. Give ownership to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# 6. Update Nginx configuration
# We use 'printf' to handle the multiline block and 'sed' to inject it
# The check prevents adding the block multiple times if the script is rerun
NGINX_CONF="/etc/nginx/sites-available/default"
STATIC_BLOCK="location 127.0.0.1/hbnb_static {\n\talias /data/web_static/current/;\n}"

if ! grep -q "location 127.0.0.1/hbnb_static" "$NGINX_CONF"; then
    sudo sed -i "/server_name _;/a \\\n\t$STATIC_BLOCK" "$NGINX_CONF"
fi

# 7. Test configuration and restart Nginx
sudo nginx -t && sudo service nginx restart
