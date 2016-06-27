"""
Provides access to common loggers across modules (which may run in
separate processes).

Usage:

    from settings.loggers import logger
    logger.debug('Diagnostics information')
    logger.info('Everything works as expected')
    logger.warning(('Something unexpected happened, or an error might '
                    'happen soon, but the software still works as '
                    'expected.'))
    logger.error('Some function could not be performed.')
    logger.critical(('A serious error. The app might be unable to '
                     'continue running.'))

The environment variable 'LOGGING_LEVEL' is the minimum severity level
of a log message for it to be output to the logging handlers.
Must be one of: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
"""

import logging
import os

logging_level = getattr(logging, os.getenv('LOGGING_LEVEL'))

simple_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
)

extended_formatter = logging.Formatter(('%(asctime)s '
    '[line %(lineno)d in %(module)s (function %(funcName)s)] '
    '%(message)s'))

# Note that we must set both the level of the logger and the handler.
logger = logging.getLogger('default_logger')
logger.setLevel(logging_level)
console_output = logging.StreamHandler()
console_output.setLevel(logging_level)
console_output.setFormatter(simple_formatter)
logger.addHandler(console_output)
