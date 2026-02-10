#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    # Create the timestamp string: YYYYMMDDHHMMSS
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Define the archive path
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    try:
        # Create 'versions' folder if it doesn't exist
        if not os.path.exists("versions"):
            local("mkdir -p versions")

        # Create the .tgz archive
        # -c: create, -v: verbose, -z: gzip, -f: file
        print("Packing web_static to {}".format(archive_path))
        local("tar -cvzf {} web_static".format(archive_path))

        # Check if file was actually created
        if os.path.exists(archive_path):
            return archive_path
        else:
            return None

    except Exception:
        return None
