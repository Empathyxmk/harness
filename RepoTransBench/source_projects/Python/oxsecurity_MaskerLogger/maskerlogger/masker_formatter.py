import logging
import re
import os

try:
    from maskerlogger.ahocorasick_regex_match import RegexMatcher
except Exception:
    RegexMatcher = None

SKIP_MASK = "MASKERLOGGER_SKIP_MASK"

class AbstractMaskedLogger:
    def __init__(self, regex_config_path: str = None, redact=40):
        self.redact = redact
        self._matcher = RegexMatcher(regex_config_path, redact) if RegexMatcher is not None else None

    def _mask_secret(self, msg, matches):
        for m in matches:
            start, end = m.span(1 if m.lastindex else 0)
            msg = msg[:start] + "*" * (end - start) + msg[end:]
        return msg

    def _mask_sensitive_data(self, record):
        msg = record.getMessage() if hasattr(record, "getMessage") else str(record.msg)
        if hasattr(record, "apply_mask") and record.apply_mask is False:
            return msg
        if self._matcher is not None:
            matches = self._matcher.find_matches(msg)
            if matches:
                record.msg = self._mask_secret(msg, matches)
        return msg

class MaskerFormatter(logging.Formatter, AbstractMaskedLogger):
    def __init__(self, fmt=None, datefmt=None, regex_config_path=None, redact=40):
        logging.Formatter.__init__(self, fmt, datefmt=datefmt)
        AbstractMaskedLogger.__init__(self, regex_config_path, redact)

    def format(self, record):
        self._mask_sensitive_data(record)
        return super().format(record)

class MaskerFormatterJson(MaskerFormatter):
    def format(self, record):
        if hasattr(record, "apply_mask") and record.apply_mask is False:
            return MaskerFormatter.format(self, record)  # Fixed: call the correct parent method
        # mask sensitive data
        self._mask_sensitive_data(record)
        return super().format(record)