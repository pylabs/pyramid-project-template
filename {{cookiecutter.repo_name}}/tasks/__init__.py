import re

from invoke import Collection, task

from {{ cookiecutter.repo_name }}.tests.helper import get_ini_settings, import_test_db_data
from . import db, test


@task
def deploy(c, ini_file):
    """Deploy project"""

    c.run('git pull origin master')
    c.run('systemctl stop uwsgi')
    c.run('alembic -c {} upgrade head'.format(ini_file))
    c.run('pipenv sync')
    c.run('systemctl start uwsgi')


namespace = Collection(deploy, db, test)
