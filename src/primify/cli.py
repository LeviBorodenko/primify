# -*- coding: utf-8 -*-

import argparse
import sys
from pathlib import Path

from primify import __version__
from primify.base import PrimeImage

__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Command-line tool for converting images to primes",
        epilog="Made by Levi B.",
    )

    parser.add_argument(
        "--image",
        action="store",
        type=Path,
        default="./prime.png",
        help="Source image to be converted",
        dest="image_path",
    )

    parser.add_argument(
        "--max_digits",
        action="store",
        type=int,
        default=5000,
        help="Maximal number of digits the prime can have",
        dest="max_digits",
    )

    parser.add_argument(
        "--output_file",
        action="store",
        type=Path,
        default="prime.txt",
        help="File name of the file containing the prime.",
        dest="output_file",
    )

    parser.add_argument(
        "-v", action="store_true", dest="verbose", help="Verbose output"
    )

    return parser.parse_args(args)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)

    a = PrimeImage(
        image_path=args.image_path,
        max_digits=args.max_digits,
        conversion_method=args.method,
        verbose=args.verbose,
        output_file_path=args.output_file,
    )

    a.get_prime()


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
