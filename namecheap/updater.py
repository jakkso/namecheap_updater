"""
Contains Updater class' implementation
"""

import logging
from logging.handlers import RotatingFileHandler
from os import environ
from pathlib import Path
from time import sleep
from typing import List
from xml.etree import ElementTree as Et

from requests import get, Response

from namecheap.message import send_message


class Updater:
    """
    Contains methods to generate a requests to update namecheap.com's
    DNS records for a list of sites
    """

    def __init__(self, domains: List[str]) -> None:
        self.domains = domains
        self.logger = None
        self.ip = None

    def __str__(self) -> str:
        return f'Updater for: `{ "` `".join(self.domains)}`'

    @staticmethod
    def _verify_env() -> None:
        """
        Verifies that the environmental variables used by this class are set
        :raises AttributeError
        """
        for var in ['dyn-password', 'log_dir']:
            if environ.get(var) is None:
                raise AttributeError(f'Environmental variable `{var}` not set')

    def get_ip(self) -> str:
        """
        Gets this computer's external IP address via api call to ipify.com
        """
        resp = get('http://api.ipify.org')
        if resp.status_code == 200:
            return resp.text
        return ''

    def _logger_setup(self) -> None:
        """
        Initiates logger
        """
        self._verify_env()  # Raises Attribute error if env vars not set
        log_dir = Path(environ['log_dir'])
        if not log_dir.exists():
            log_dir.mkdir()
        filename = Path.joinpath(log_dir, 'namecheap-updater.log')
        log = logging.getLogger('namecheap_updater')
        log.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(filename)s] func: [%(funcName)s] [%(levelname)s] "
                                "line: [%(lineno)d] %(message)s")
        file_handler = RotatingFileHandler(filename=filename,
                                           delay=True,
                                           backupCount=5,
                                           maxBytes=2000000)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        if not log.handlers:
            log.addHandler(file_handler)
        self.logger = log

    def _send_request(self, domain: str, ip: str) -> Response:
        """
        Returns response to get request sent to the update URL
        :param domain: string of domain for which to request an update
        :param ip: string of new ip address
        """
        update_url = f'https://dynamicdns.park-your-domain.com/update?' \
                     f'host=@&domain={domain}&password={environ["dyn-password"]}&ip={ip}'
        return get(update_url)

    def run(self) -> None:
        """

        """
        self._logger_setup()
        for _ in range(3):
            ip = self.get_ip()
            if ip:
                self.ip = ip
                self.logger.info('IP fetched successfully')
                break
            else:
                self.logger.warning(f'IP fetch attempt unsuccessful, trying again in 2 seconds...')
                sleep(2)
        if not self.ip:
            raise AttributeError('Unable to fetch IP address')

        while True:
            old_ip = self.ip
            new_ip = self.get_ip()
            if old_ip != new_ip:
                # Requests must be sent.
                successes = 0
                failures = []
                for domain in self.domains:
                    resp = self._send_request(domain, new_ip)
                    success = xml_errors(resp.text)
                    if success:
                        msg = f'IP address change for {domain} submitted to namecheap, ' \
                              'change should be effective in 30 minutes.'
                        self.logger.info(msg)
                        successes += 1
                    else:
                        msg = f'IP address request failure, response: {resp.text}'
                        failures.append(msg)
                        self.logger.error(msg)
                if successes == len(self.domains):
                    msg = f'IP address change for domains: {" ".join(self.domains)}\nsuccessful updated to {new_ip}'
                    send_message('Namecheap DynDNS IP address change successful', msg)
                    self.ip = new_ip
                else:

                    msg = f'Namecheap DynDNS IP address change failed!\n' + "\n".join(failures)
                    send_message('Namecheap DynDNS IP address change Failure!', msg)
            else:
                self.logger.info('IP address same, sleeping')
            sleep(300)


def xml_errors(xml: str) -> bool:
    """
    Parses XML, determines if the xml response contains errors.
    :param xml: string, xml response returned from namecheap dns update request
    :return:
    """
    for child in Et.fromstring(xml):
        if child.tag == 'ErrCount':
            return not child.text == '0'
