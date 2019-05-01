from pyramid import testing

from {{ cookiecutter.repo_name }}.views.home import home_view

def test_home_view():
    info = home_view(testing.DummyRequest())
    assert info == {'project': '{{ cookiecutter.project_name }}'}
    
