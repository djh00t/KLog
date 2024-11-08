# klog/custom_logger.py

import logging


class CustomLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, **kwargs):
        if extra is None:
            extra = {}
        # Merge kwargs into extra and ensure msg_content is set
        extra.update(kwargs)
        extra['msg_content'] = msg
        super()._log(level, msg, args, exc_info=exc_info, extra=extra)

    def debug(self, message, *args, **kwargs):
        self._log(logging.DEBUG, message, args, **kwargs)

    def info(self, message, *args, **kwargs):
        self._log(logging.INFO, message, args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self._log(logging.WARNING, message, args, **kwargs)

    def error(self, message, *args, **kwargs):
        self._log(logging.ERROR, message, args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self._log(logging.CRITICAL, message, args, **kwargs)
