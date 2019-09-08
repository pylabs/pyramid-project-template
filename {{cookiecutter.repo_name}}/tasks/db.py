import re

from invoke import task

from {{ cookiecutter.repo_name }}.tests.helper import get_ini_settings, import_test_db_data


def find_ini_file():                                                                                                                            
    if os.path.exists('production.ini'):                                                                                                        
        return 'production.ini'                                                                                                                 
    elif os.path.exists('development.ini'):                                                                                                     
        return 'development.ini'                                                                                                                
    else:                                                                                                                                       
        raise ParseError('--ini-file should be valid file path')


@task(name='create', optional=['ini_file'])
def db_create(c, ini_file=None):
    """Create database"""

    if ini_file is None:
        ini_file = find_ini_file()

    # Find database name via ini file
    sqlalchemy_url = get_ini_settings(ini_file)['sqlalchemy.url']
    db_name = re.findall(r'/(\w+)\?', sqlalchemy_url)[0]
    db_user, db_pass = re.findall(r'//(\w+):(\w+)@', sqlalchemy_url)[0]
    c.run('sudo mysql -uroot -e "CREATE DATABASE IF NOT EXISTS {} CHARSET utf8mb4"'.format(db_name))
    c.run('sudo mysql -uroot -e "GRANT ALL ON {0}.* to {1}@localhost '
          'IDENTIFIED BY \'{2}\'"'.format(db_name, db_user, db_pass))


@task(name='delete', optional=['ini_file'])
def db_delete(c, ini_file=None):
    """Delete database"""

    if ini_file is None:
        ini_file = find_ini_file()

    sqlalchemy_url = get_ini_settings(ini_file)['sqlalchemy.url']
    db_name = re.findall(r'/(\w+)\?', sqlalchemy_url)[0]
    c.run('sudo mysql -uroot -e "DROP DATABASE IF EXISTS {}"'.format(db_name))


@task(db_delete, db_create, name='init', optional=['ini_file'])
def init_db(c, ini_file=None):
    """Create database and import basic data"""

    if ini_file is None:
        ini_file = find_ini_file()

    c.run('alembic -c {} upgrade head'.format(ini_file))
    c.run('initialize_{{ cookiecutter.repo_name }}_db {}'.format(ini_file))


@task(db_delete, db_create, name='init-test', optional=['ini_file'])
def init_test_db(c, ini_file=None):
    """Create database and import test data"""

    if ini_file is None:
        ini_file = find_ini_file()

    c.run('alembic -c {} upgrade head'.format(ini_file))
    import_test_db_data(ini_file)

