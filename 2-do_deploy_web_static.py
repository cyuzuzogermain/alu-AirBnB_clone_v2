#!/usr/bin/python3
from fabric.api import env, put, run
import os

# Define your server IPs here
env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # 1. Get filename and folder name from path
        # Example: archive_path = versions/web_static_2024.tgz
        # file_name = web_static_2024.tgz, folder_name = web_static_2024
        file_name = os.path.basename(archive_path)
        folder_name = file_name.split(".")[0]
        remote_tmp = "/tmp/{}".format(file_name)
        release_path = "/data/web_static/releases/{}/".format(folder_name)

        # 2. Upload the archive to /tmp/
        put(archive_path, remote_tmp)

        # 3. Create the release folder and uncompress
        run("mkdir -p {}".format(release_path))
        run("tar -xzf {} -C {}".format(remote_tmp, release_path))

        # 4. Delete the archive from /tmp/
        run("rm {}".format(remote_tmp))

        # 5. Move files out of the internal 'web_static' folder and cleanup
        # tar usually wraps things in a 'web_static' folder based on how we packed it
        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))

        # 6. Delete old symbolic link
        run("rm -rf /data/web_static/current")

        # 7. Create new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception:
        return False
