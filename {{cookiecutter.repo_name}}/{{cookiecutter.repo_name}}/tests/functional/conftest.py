import os
import subprocess

import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


@pytest.fixture(scope='session', autouse=True)
def create_db():
    """Create a database for test purpose."""

    sql_file_path = os.path.join(FIXTURES_DIR, 'create_test_database.sql')
    subprocess.run(f'sudo mysql -uroot < {sql_file_path}', shell=True)
