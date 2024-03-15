#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        archive_file = archive_path.split('/')[-1]
        folder_name = '/data/web_static/releases/{}'.format(archive_file.split('.')[0])
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(archive_file, folder_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_file))

        # Move the contents of the uncompressed folder to its parent directory
        run('mv {}/web_static/* {}'.format(folder_name, folder_name))

        # Remove the empty folder created during the extraction
        run('rm -rf {}/web_static'.format(folder_name))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version of your code
        run('ln -s {} /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True
    except:
        return False
