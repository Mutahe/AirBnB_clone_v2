#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['54.173.86.102', '54.157.166.185']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school' 

def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        # Put the archive in /tmp directory of remote server
        print(f"Putting {archive_path} to /tmp/")
        put(archive_path, '/tmp/')

        # Create directory for the new release
        print(f"Creating directory for the new release: {path}{no_ext}/")
        run('mkdir -p {}{}/'.format(path, no_ext))

        # Extract the archive to the new release directory
        print(f"Extracting archive to {path}{no_ext}/")
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))

        # Remove the archive from /tmp directory
        print(f"Removing {file_n} from /tmp/")
        run('rm /tmp/{}'.format(file_n))

        # Move contents of web_static directory to the new release directory
        print(f"Moving contents of {path}{no_ext}/web_static/* to {path}{no_ext}/")
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))

        # Remove the now-empty web_static directory
        print(f"Removing {path}{no_ext}/web_static")
        run('rm -rf {}{}/web_static'.format(path, no_ext))

        # Remove the current symbolic link
        print("Removing current symbolic link")
        run('rm -rf /data/web_static/current')

        # Create new symbolic link pointing to the new release directory
        print(f"Creating new symbolic link to {path}{no_ext}/")
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

