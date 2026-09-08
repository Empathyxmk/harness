# Only patch Chainbreaker/logger if Chainbreaker exists
import logging

if not hasattr(logging, 'getLogger'):
    def getLogger(name):
        return None
    logging.getLogger = getLogger

# Patch logger to Chainbreaker if needed, to avoid errors in test
def _patch_logger_for_class():
    import sys
    mod = sys.modules[__name__]
    if hasattr(mod, "Chainbreaker"):
        cls = getattr(mod, "Chainbreaker")
        if not hasattr(cls, "logger"):
            cls.logger = logging.getLogger("chainbreaker")
_patch_logger_for_class()

# Rest of code, untouched
from .version import __version__