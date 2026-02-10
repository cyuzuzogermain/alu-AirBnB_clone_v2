#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers.
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os

# Replace these with your actual server IP addresses
env.hosts = ['34.205.24.28', '34.239.101.72']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        if not os.path.exists("versions"):
            local("mkdir -p versions")

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(now)

        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract filename and folder names
        file_name = os.path.basename(archive_path)
        folder_name = file_name.split(".")[0]
        remote_tmp = "/tmp/{}".format(file_name)
        release_path = "/data/web_static/releases/{}".format(folder_name)

        # Upload and uncompress
        put(archive_path, remote_tmp)
        run("mkdir -p {}/".format(release_path))
        run("tar -xzf {} -C {}/".format(remote_tmp, release_path))
        run("rm {}".format(remote_tmp))

        # Move content out of web_static and delete internal folder
        run("mv {}/web_static/* {}/".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))

        # Update symbolic link
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
