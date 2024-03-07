#!/usr/bin/python3
"""a fabric scrip to execute a tgz archive file"""

from datetime import datetime
from fabric.api import *
import os

def do_pack():
    time = datetime.now()
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('sudo mkdir -p versions')
    filemade = local('tar -cvzf versions/{} web_static'.format(archive))
    
    if filemade != None:
        return archive
    else:
        return None