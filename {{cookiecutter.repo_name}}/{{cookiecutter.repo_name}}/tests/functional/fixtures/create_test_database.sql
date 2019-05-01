DROP DATABASE IF EXISTS test_{{ cookiecutter.repo_name }};
CREATE DATABASE test_{{ cookiecutter.repo_name }} CHARSET utf8mb4;
GRANT ALL ON test_{{ cookiecutter.repo_name }}.* to test_{{ cookiecutter.repo_name }} IDENTIFIED BY 'test_{{ cookiecutter.repo_name }}';
