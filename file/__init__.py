#!/usr/bin/env python3


"""Get and serve files
"""

from ftplib import FTP
from typing import List
from flask import Blueprint, render_template
from flask_login import login_required  # type: ignore


racer_file = Blueprint('racer_file', __name__, url_prefix='/file')

ftp = FTP()
ftp.connect(
    host='localhost', port=2121)
ftp.login(user='anonymous', passwd='anonymous@')


@racer_file.get('/')
@login_required
def file_manager():
    """Lists all files in the"""

    return render_template('file_manager.html', files=list_files())


def list_files() -> list:
    """Lists all files in the"""
    data: List[str] = list()
    obj_list = []

    ftp.retrlines('LIST', data.append)

    for line in data:
        parts = line.split()
        obj = {
            'permissions': parts[0],
            'links': int(parts[1]),
            'ownerId': int(parts[2]),
            'groupId': int(parts[3]),
            'size': int(parts[4]),
            'month': parts[5],
            'day': int(parts[6]),
            'timeOrYear': parts[7],
            'name': ' '.join(parts[8:])
        }

        obj_list.append(obj)

    return obj_list
