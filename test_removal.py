from shutil import rmtree
from os import makedirs
import sys

rmtree(f"{sys.path[0]}/temp")
makedirs(f"{sys.path[0]}/temp")