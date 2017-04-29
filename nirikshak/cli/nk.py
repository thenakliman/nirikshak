import argparse
import sys

from nirikshak.common import configurations as config


def process_args():
    parser = argparse.ArgumentParser(description='Process nirikshak command'
                                                 'line arguments')

    parser.add_argument('--tags', metavar='t', type=str, nargs='+',
                        help='list of tags for jaanch')
    parser.add_argument('--soochi', metavar='s', type=str, nargs='+',
                        help='list of soochi for execute')

    return parser.parse_args()


def main():
    args = process_args()
    dir(nirikshak)
    help(nirikshak)
    config.initilize_config()
    config.initilize_logging()

if __name__ == "__main__":
    main()
