"""
This module demonstrates handling secrets in logs with ox_formatter.
"""

import logging
from maskerlogger.masker_formatter import MaskerFormatter, SKIP_MASK

def log_sensitive():
    logger = logging.getLogger("test_logger")
    handler = logging.StreamHandler()
    handler.setFormatter(MaskerFormatter("%(message)s", regex_config_path=None))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info("this password: myplaintextpassword should be masked")
    logger.info("no secrets here")
    logger.info("the value to skip", extra={"apply_mask": False})

def main():
    log_sensitive()

if __name__ == "__main__":
    main()