#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of the AirBnB Clone project.
"""

from fabric import task
import os
from datetime import datetime


@task
def do_pack(c):
    """
    Generates a .tgz archive from web_static
    Returns the archive path if successful, otherwise None
    """
    try:
        # Create versions directory if it does not exist
        if not os.path.isdir("versions"):
            os.mkdir("versions")

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Archive filename
        archive = f"versions/web_static_{timestamp}.tgz"

        # Create the archive
        result = c.local(f"tar -cvzf {archive} web_static", hide=True)

        if result.ok:
            return archive
        else:
            return None

    except Exception:
        return None
