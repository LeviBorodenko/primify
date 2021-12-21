# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound
import logging
from rich.console import Console

console = Console()


FORMAT = "%(message)s"
logging.basicConfig(level="DEBUG", format=FORMAT, datefmt="[%X]", filename="logs.txt")
try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
