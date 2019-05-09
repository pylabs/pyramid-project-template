import os, re

from invoke import Collection, task
from invoke.exceptions import ParseError

from {{ cookiecutter.repo_name }}.tests.helper import get_ini_settings, import_test_db_data

from . import db, test


@task(optional=['ini_file'])
def deploy(c, ini_file=None):
    """Deploy project"""

    if ini_file is None:
        if os.path.exists('production.ini'):
            ini_file = 'production.ini'
        elif os.path.exists('development.ini'):
            ini_file = 'development.ini'
        else:
            raise ParseError('--ini-file should be valid ini file path')

    c.run('git pull origin master')
    c.run('systemctl stop uwsgi')
    c.run('alembic -c {} upgrade head'.format(ini_file))
    c.run('pipenv sync')
    c.run('systemctl start uwsgi')


namespace = Collection(deploy, db, test)

