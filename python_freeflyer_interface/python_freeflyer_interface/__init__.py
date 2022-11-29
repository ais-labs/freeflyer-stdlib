"""
Basic setup for the entire module.
"""

# native imports
import logging


# third party imports


# local imports




# set up logging for application
logging.basicConfig(
    format='[python]%(asctime)s.%(msecs)03d [%(levelname)5.5s] '+ \
           '[%(name)-25.25s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
)


log = logging.getLogger(__name__)
