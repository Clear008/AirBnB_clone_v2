#!/usr/bin/python3
"""creates and distributes an archive to your web servers"""
from fabric.api import put, run, env, local
from fabric.contrib.files import exists
from datetime import datetime
import os

env.hosts = ['18.206.208.113', '18.206.232.93']
env.user = "ubuntu"


def do_pack():
    """Creates an archive from the contents of the web_static folder."""
    try:
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        if not os.path.exists("versions"):
            local("mkdir versions")
        archive_p = 'versions/web_static_{}.tgz'.format(time)
        local("tar -czvf {} web_static".format(archive_p))
        return archive_p
    except FileNotFoundError:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except FileNotFoundError:
        return False


def deploy():
    """ DEPLOYS """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
