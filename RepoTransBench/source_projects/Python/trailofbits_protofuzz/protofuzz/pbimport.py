"""
pbimport.py: Import utilities for protos in protofuzz
"""
import os
import re

def import_proto_module(proto_file):
    # Dummy implementation for testing
    # Would use actual protobuf in real usage.
    class DummyMsg:
        DESCRIPTOR = "Dummy"
    return DummyMsg

def resolve_include_path(filename, include_paths):
    for path in include_paths:
        full = os.path.join(path, os.path.basename(filename))
        if os.path.exists(full):
            return full
    return None

def parse_proto_imports(proto_content):
    return re.findall(r'import\s+"([^"]+)";', proto_content)