#!/usr/bin/python3
"""Distributes an archive to your web servers"""
from fabric.api import run, put, env
from datetime import datetime
import os


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        archive_name = os.path.basename(archive_path)
        archive_base = os.path.splitext(archive_name)[0]
        path = "/data/web_static/releases/"

        run('mkdir -p {}{}/'.format(path, archive_base))
        run('tar -xzf /tmp/{} -C {}{}/'
            .format(archive_name, path, archive_base))
        run('rm /tmp/{}'.format(archive_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, archive_base))

        print("New version deployed!")
        return True
    except FileNotFoundError:
        return False