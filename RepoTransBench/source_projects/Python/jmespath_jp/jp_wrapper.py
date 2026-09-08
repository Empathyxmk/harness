import subprocess
import json

class JpWrapper:
    """
    Python wrapper for the jp binary (Go implementation of jmespath command line).
    Allows invoking jp with JSON input and queries from Python code.
    """

    def __init__(self, jp_binary='./jp'):
        self.jp_binary = jp_binary

    def search(self, query, data):
        """
        Run jp on JSON data with the provided JMESPath query.

        :param query: JMESPath string
        :param data: JSON-serializable Python data
        :return: Decoded JSON result or None if not JSON
        :raises: Exception on jp error or execution failure
        """
        input_str = json.dumps(data)
        try:
            p = subprocess.run(
                [self.jp_binary, query],
                input=input_str.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=3
            )
            if p.returncode != 0:
                raise Exception(f"jp error: {p.stderr.decode('utf-8')}")
            output = p.stdout.decode('utf-8').strip()
            # Try decode JSON, fallback to string
            try:
                return json.loads(output)
            except Exception:
                return output
        except Exception as e:
            raise Exception(f"jp invocation failed: {e}")