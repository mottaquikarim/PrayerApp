from os import environ

from prayerapp.main import foobar


def test_env_vars_exist():
    assert environ.get('TEST') == '1'


def test_foobar():
    assert foobar() == 418
