"""
log.py: Minimal debug logging for protofuzz
"""

DEBUG_ENABLED = False

def set_level_debug(enabled=True):
    global DEBUG_ENABLED
    DEBUG_ENABLED = enabled

def debug(msg):
    if DEBUG_ENABLED:
        print("[protofuzz:DEBUG]", msg)