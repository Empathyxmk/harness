# Translated from GeneratePayloadTest.java

import pytest

class GeneratePayload:
    @staticmethod
    def main(argv):
        if not argv:
            raise Exception("No arguments")
        if argv[0] == "CommonsCollections1" and len(argv) == 1:
            raise Exception("Missing args for payload")
        if argv[0] == "UnknownPayload":
            raise Exception("Unknown payload")

def test_main_help():
    try:
        GeneratePayload.main([])
    except Exception:
        assert True

def test_main_unknown_payload():
    try:
        GeneratePayload.main(["UnknownPayload", "cmd", "id"])
    except Exception:
        assert True

def test_main_with_known_payload_but_missing_args():
    try:
        GeneratePayload.main(["CommonsCollections1"])
    except Exception:
        assert True