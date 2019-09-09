from invoke import Collection, task

from . import db, test
from .helper import find_ini_file


@task(optional=['ini_file'])
def deploy(c, ini_file=None):
    """Deploy project"""

    if ini_file is None:
        ini_file = find_ini_file()

    c.run('git pull origin master')
    c.run('systemctl stop uwsgi')
    c.run('alembic -c {} upgrade head'.format(ini_file))
    c.run('pipenv sync')
    c.run('systemctl start uwsgi')


namespace = Collection(deploy, db, test)

