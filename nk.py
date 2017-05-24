import argparse
import logging
import sys

from nirikshak.controller import base


def process_args():
    parser = argparse.ArgumentParser(description='Process nirikshak command'
                                                 'line arguments')

    parser.add_argument('--tags', metavar='t', type=str, nargs='+',
                        default=[], help='List of tags for jaanch')
    parser.add_argument('--soochis', metavar='s', type=str, nargs='+',
                        default=[], help='List of soochi for verification')
    parser.add_argument('--config-file', metavar='c', type=str,
                        default=[], help='Path of configuration '
                        'file for nirikshak')
    parser.add_argument('--groups', metavar='g', type=str, nargs='+',
                        default=[], help='List of groups to be executed')

    return parser.parse_args()


def main():
    args = process_args()
    base.Router().start(**vars(args))
    logging.info("Jaanch has been finished, check results")

if __name__ == "__main__":
    main()
