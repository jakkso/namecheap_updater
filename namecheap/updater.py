"""
Contains methods to update the dynamic DNS records of namecheap.com
"""

import datetime
import logging
from logging.handlers import RotatingFileHandler
from os import environ
from pathlib import Path
from time import sleep

from requests import get
from namecheap.message import send_message


class Updater:
    """
    Contains methods to update the list of namecheap urls
    """
    nc_url = "http://dynamicdns.park-your-domain.com"

    def __init__(self, *args):
        self.domains = [i for i in args]
        self.logger = self._logger()

    def __str__(self):
        return f'Update for {len(self.domains)}'

    @property
    def _my_ip(self):
        """
        Gets this client's external IP address via api calls to ipify.com
        """
        url = 'http://api.ipify.org'
        resp = get(url)
        if resp.status_code == 200:
            return resp.text
        else:
            return ''

    @staticmethod
    def _logger() -> logging.getLogger:
        """
        Initiates logger
        """

        def logger_location() -> Path:
            """
            Initializer for logger's location, which is in $HOME/logs/namecheap-updater.log
            """
            log_dir = Path.joinpath(Path.home(), 'logs')
            if not log_dir.exists():
                log_dir.mkdir()
            return Path.joinpath(log_dir, 'namecheap-updater.log')

        log = logging.getLogger('namecheap_updater')
        log.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(filename)s] func: [%(funcName)s] [%(levelname)s] "
                                "line: [%(lineno)d] %(message)s")
        filename = logger_location()
        file_handler = RotatingFileHandler(filename=filename,
                                           delay=True,
                                           backupCount=5,
                                           maxBytes=2000000)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        if not log.handlers:
            log.addHandler(file_handler)
        return log

    def run(self) -> None:
        """
        Gets ip address, runs update subroutine
        """
        my_ip_addr = self._my_ip
        if not my_ip_addr:
            msg = 'Unable to fetch ip address'
            self.logger.log(logging.ERROR, msg)
            send_message('Namecheap update process failure', msg)
            return print(msg)
        while True:
            if my_ip_addr == self._my_ip:
                sleep(600)
                my_ip_addr = self._my_ip
            else:
                timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                my_ip_addr = self._my_ip
                msg = f'{timestamp} Changed IP to {my_ip_addr}'
                self.logger.log(logging.INFO, msg)
                print(msg)
                send_message('DynDNS IP address change', msg)

                for url in self.domains:
                    update_url = f'{self.nc_url}/update?host=@' \
                                 f'&domain={url}' \
                                 f'&password={environ["dyn-password"]}' \
                                 f'&ip={my_ip_addr}'
                    resp = get(update_url)

