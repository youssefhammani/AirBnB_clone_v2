#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
from fabric.api import env, lcd, local, run
from datetime import datetime
import os

env.hosts = ['<IP web-01>', 'IP web-02']
env.user = 'ubuntu'  # Username for accessing the server
env.key_filename = ['my_ssh_private_key']  # SSH key for accessing the server


def do_clean(number=0):
    """
    Deletes out-of-date archives from the server.

    Args:
        number (int): Number of archives to keep (default is 0).
    """
    number = int(number)
    if number < 1:
        number = 1

    # Delete out-of-date archives in versions folder
    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs -d '\n' rm -rf".format(number + 1))

    # Delete out-of-date archives in web_static/releases folder
    archives = sorted(run("ls -t /data/web_static/releases").split())
    to_delete = archives[:-number] if len(archives) > number else []
    for archive in to_delete:
        run("rm -rf /data/web_static/releases/{}".format(archive))

    # Delete symbolic link to current release in web_static folder
    current_release = run("ls -l /data/web_static/current").split()[-1]
    if current_release in to_delete:
        run("rm /data/web_static/current")
