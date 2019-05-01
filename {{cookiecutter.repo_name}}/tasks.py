from invoke import task


@task
def test(c):
    c.run('pytest')

@task
def test_coverage(c):
    c.run('pytest --cov={{ cookiecutter.repo_name }}')
