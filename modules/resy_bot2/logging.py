import logging
import sys
from rich.logging import RichHandler

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(handlers=[RichHandler()], level=logging.DEBUG)

