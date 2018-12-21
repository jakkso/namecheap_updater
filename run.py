"""
Entrypoint for program
"""

from namecheap.updater import Updater

if __name__ == '__main__':
    domain_file = '/usr/src/app/domains.txt'
    with open(domain_file) as file:
        domains = [line.strip() for line in file]
    up = Updater(domains)
    try:
        up.run()
    except AttributeError as e:
        print(e)
