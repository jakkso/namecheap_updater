"""
Contains tests for Updater
"""
from namecheap.updater import Updater


def test_str() -> None:
    """
    Checking that the str method is formatted correctly.
    """
    domains = ['hello.com', 'hi.com']
    up = Updater(domains)
    assert up.__str__() == 'Updater for: `hello.com` `hi.com`'
    up = Updater(['hello.com'])
    assert str(up) == 'Updater for: `hello.com`'


def test_get_ip()-> None:
    """
    Checks that get_up returns a string
    """
    up = Updater(['1.com', '2.com'])
    up.ip = up.get_ip()
    assert up.ip is not None  # This depends on the ipify.org API working.

