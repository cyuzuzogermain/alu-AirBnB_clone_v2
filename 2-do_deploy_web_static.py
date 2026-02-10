#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os

# Define your server IPs
env.hosts = ['34.205.24.28', '34.239.101.72']
env.user = 'ubuntu'

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(now)

        if not os.path.exists("versions"):
            local("mkdir -p versions")

        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        # Get filename info
        file_name = os.path.basename(archive_path)
        folder_name = file_name.split(".")[0]
        remote_tmp = "/tmp/{}".format(file_name)
        release_path = "/data/web_static/releases/{}/".format(folder_name)

        # 1. Upload
        put(archive_path, remote_tmp)

        # 2. Uncompress and setup directory
        run("mkdir -p {}".format(release_path))
        run("tar -xzf {} -C {}".format(remote_tmp, release_path))
        run("rm {}".format(remote_tmp))

        # 3. Flatten the structure (Move files out of web_static subfolder)
        # This ensures /hbnb_static/0-index.html works correctly
        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))

        # 4. Update symbolic link
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        return True
    except Exception:
        return False

def deploy():
    """Runs the full pack and deploy process."""
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
