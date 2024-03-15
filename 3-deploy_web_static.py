#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers"""

from fabric.api import local, env, put, run
from datetime import datetime
import os

# Set the username and SSH key
env.user = 'ubuntu'
env.key_filename = '~/.ssh/my_ssh_private_key'

# List of web servers
env.hosts = ['xx.xx.xx.xx', 'xx.xx.xx.xx']


def do_pack():
    """Create a compressed archive of web_static contents"""
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(current_time)
        local('mkdir -p versions')
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Distribute an archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_name)[0]
        release_path = '/data/web_static/releases/{}'.format(archive_no_ext)

        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, release_path))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {}/web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}/web_static'.format(release_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))

        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():
    """Create and distribute an archive to web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
