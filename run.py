"""
Entry-point for program
"""

from os import environ

from namecheap.updater import Updater

if __name__ == '__main__':
    try:
        domain_file = environ['domain_file']
        with open(domain_file) as file:
            domains = [line.strip() for line in file]
        up = Updater(domains)
        up.run()
    except KeyError as e:
        print(f'env vars not set: {e}')
    except AttributeError as e:
        print(e)
    except KeyboardInterrupt:
        print('\nQuitting')
