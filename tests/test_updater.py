"""
Contains tests for Updater
"""
from namecheap.updater import Updater, xml_errors


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


def test_xml_parser() -> None:
    """
    Checks that the XML parsers correctly detects errors as it should, i.e.,
    if the <ErrCount> tag contains 0, False is returned, otherwise True
    """
    success_xml = '<?xml version="1.0"?><interface-response><Command>SETDNSHOST</Command><Language>eng</Language><IP>127.0.0.1</IP><ErrCount>0</ErrCount><ResponseCount>0</ResponseCount><Done>true</Done><debug><![CDATA[]]></debug></interface-response>'
    fail_xml = '<?xml version="1.0"?><interface-response><Command>SETDNSHOST</Command><Language>eng</Language><IP>127.0.0.1</IP><ErrCount>1</ErrCount><ResponseCount>0</ResponseCount><Done>true</Done><debug><![CDATA[]]></debug></interface-response>'
    assert xml_errors(success_xml) is False
    assert xml_errors(fail_xml) is True

