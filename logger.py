# encoding: utf-8
"""
Logging module

Initialises logging handlers for a rotating file log and stdout log.
"""
import logging
import logging.handlers
import os
import sys


class FilePrintLogger(object):
    """Logger delegation class to set up a print log and file log."""

    def __init__(self, logger_name, print_level=logging.INFO, file_path='.',
                 file_level=logging.INFO):
        """Set up the instance with a logger name.

        Optionally set the print level, log file path and log file level.

        """
        # Sets the root logger and a log file
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(logging.DEBUG)

        # Create a stdout logger to avoid print
        self._print_log = logging.StreamHandler(sys.stdout)
        self._print_log.setFormatter(logging.Formatter('%(message)s'))
        self._logger.addHandler(self._print_log)

        self.set_print_handler_level(print_level)
        self.set_file_handler(file_path, file_level)

    def __getattr__(self, name):
        """Support delegation to logger."""
        return getattr(self._logger, name)

    def set_print_handler_level(self, level):
        """Set the logging level of the print logger."""
        self._print_log.setLevel(level)

    def set_file_handler(self, path, level):
        """Set the logging path and level of the file log."""
        os.makedirs(os.path.dirname(path), exist_ok=True)

        self._file_log = logging.handlers.RotatingFileHandler(
            path, maxBytes=1024 * 1000, backupCount=5)
        self._file_log.setLevel(level)
        log_format = logging.Formatter(
            '%(asctime)s|%(levelname)s|%(process)d|%(module)s@%(lineno)s:'
            '%(funcName)s %(message)s')
        self._file_log.setFormatter(log_format)
        self._logger.addHandler(self._file_log)


