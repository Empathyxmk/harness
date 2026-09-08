# This file represents the translation of the Java annotation PayloadTest
# In Python, this would typically be modeled as a decorator or just a data class for metadata
# but since this annotation is used as metadata for tests and doesn't affect runtime logic, we create a stub.

# In the test/translation context, this does not produce runtime tests.
# If any Python usage is intended, one might use:
from dataclasses import dataclass

@dataclass
class PayloadTest:
    skip: str = ""
    precondition: str = ""
    harness: str = ""
    flaky: str = ""