#!/usr/bin/python3
"""a fabric scrip to execute a tgz archive file"""

from datetime import datetime
from fabric.api import *
import os

@task
def do_pack():
    time = datetime.now()
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'

    with hide('running'):
        local('sudo mkdir -p versions')

    print(f"Packing web_static to versions/{archive}")

    filemade = local('tar -cvzf versions/{} web_static'.format(archive))

    file_size =  os.path.getsize(f"versions/{archive}")

    print(f"web_static packed: {archive} -> {file_size}Bytes")

    
    if filemade is not None:
        return archive

