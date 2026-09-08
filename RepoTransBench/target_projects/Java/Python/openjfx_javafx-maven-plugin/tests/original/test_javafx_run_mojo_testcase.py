import pytest

class JavaFXRunMojo:
    """
    Minimal stub for splitComplexArgumentStringAdapter for testSplitComplexArgumentString.
    In the Java code, this is either a wrapper or some pre-existing util implementation.
    Here we implement equivalent string splitting logic as needed from the original test,
    matching output for the provided test case.
    """
    def splitComplexArgumentStringAdapter(self, argument_string):
        """
        This function should split argument_string in the same way as the Java splitComplexArgumentStringAdapter,
        to pass the test case in testSplitComplexArgumentString.

        The provided argument string:
        param1 param2   \n   param3\nparam4="/path/to/my file.log"   'var"foo   var"foo' 'var"foo'   'var"foo' "foo'var foo'var" "foo'var" "foo'var"
        """
        import shlex
        # Shlex splits on POSIX unless otherwise specified.
        # It handles both quoted types and escapes nicely for our purpose.
        return shlex.split(argument_string)

def test_split_complex_argument_string():
    option = (
        "param1 "
        "param2   \n   "
        "param3\n"
        "param4=\"/path/to/my file.log\"   "
        "'var\"foo   var\"foo' "
        "'var\"foo'   "
        "'var\"foo' "
        "\"foo'var foo'var\" "
        "\"foo'var\" "
        "\"foo'var\""
    )
    expected_list = [
        "param1",
        "param2",
        "param3",
        "param4=\"/path/to/my file.log\"",
        "var\"foo   var\"foo",
        "var\"foo",
        "var\"foo",
        "foo'var foo'var",
        "foo'var",
        "foo'var"
    ]
    mojo = JavaFXRunMojo()
    result = mojo.splitComplexArgumentStringAdapter(option)
    # Insert a 'START' for accurate concatenation as in original Java reduce
    splited_option = ["START"] + result
    expected = ",".join(["START"] + expected_list)
    actual = ",".join(splited_option)
    assert actual == expected