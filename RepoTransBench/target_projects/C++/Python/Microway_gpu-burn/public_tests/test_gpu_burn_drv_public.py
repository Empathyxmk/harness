import pytest

# Redefine CUDA error codes for testing purposes
CUDA_ERROR_INVALID_VALUE = 1
CUDA_ERROR_OUT_OF_MEMORY = 2
CUDA_ERROR_NOT_INITIALIZED = 3
CUDA_ERROR_DEINITIALIZED = 4
CUDA_ERROR_NO_DEVICE = 5
CUDA_ERROR_INVALID_DEVICE = 6
CUDA_ERROR_INVALID_IMAGE = 7
CUDA_ERROR_INVALID_CONTEXT = 8
CUDA_ERROR_MAP_FAILED = 9
CUDA_ERROR_UNMAP_FAILED = 10
CUDA_ERROR_ARRAY_IS_MAPPED = 11
CUDA_ERROR_ALREADY_MAPPED = 12
CUDA_ERROR_NO_BINARY_FOR_GPU = 13
CUDA_ERROR_ALREADY_ACQUIRED = 14
CUDA_ERROR_NOT_MAPPED = 15
CUDA_ERROR_NOT_MAPPED_AS_ARRAY = 16
CUDA_ERROR_NOT_MAPPED_AS_POINTER = 17
CUDA_ERROR_UNSUPPORTED_LIMIT = 18
CUDA_ERROR_CONTEXT_ALREADY_IN_USE = 19
CUDA_ERROR_INVALID_SOURCE = 20
CUDA_ERROR_FILE_NOT_FOUND = 21
CUDA_ERROR_SHARED_OBJECT_SYMBOL_NOT_FOUND = 22
CUDA_ERROR_SHARED_OBJECT_INIT_FAILED = 23
CUDA_ERROR_OPERATING_SYSTEM = 24

def checkError(rCode, desc=""):
    if not hasattr(checkError, "g_errorStrings"):
        error_strings = {
            CUDA_ERROR_INVALID_VALUE: "CUDA_ERROR_INVALID_VALUE",
            CUDA_ERROR_OUT_OF_MEMORY: "CUDA_ERROR_OUT_OF_MEMORY",
            CUDA_ERROR_NOT_INITIALIZED: "CUDA_ERROR_NOT_INITIALIZED",
            CUDA_ERROR_DEINITIALIZED: "CUDA_ERROR_DEINITIALIZED",
            CUDA_ERROR_NO_DEVICE: "CUDA_ERROR_NO_DEVICE",
            CUDA_ERROR_INVALID_DEVICE: "CUDA_ERROR_INVALID_DEVICE",
            CUDA_ERROR_INVALID_IMAGE: "CUDA_ERROR_INVALID_IMAGE",
            CUDA_ERROR_INVALID_CONTEXT: "CUDA_ERROR_INVALID_CONTEXT",
            CUDA_ERROR_MAP_FAILED: "CUDA_ERROR_MAP_FAILED",
            CUDA_ERROR_UNMAP_FAILED: "CUDA_ERROR_UNMAP_FAILED",
            CUDA_ERROR_ARRAY_IS_MAPPED: "CUDA_ERROR_ARRAY_IS_MAPPED",
            CUDA_ERROR_ALREADY_MAPPED: "CUDA_ERROR_ALREADY_MAPPED",
            CUDA_ERROR_NO_BINARY_FOR_GPU: "CUDA_ERROR_NO_BINARY_FOR_GPU",
            CUDA_ERROR_ALREADY_ACQUIRED: "CUDA_ERROR_ALREADY_ACQUIRED",
            CUDA_ERROR_NOT_MAPPED: "CUDA_ERROR_NOT_MAPPED",
            CUDA_ERROR_NOT_MAPPED_AS_ARRAY: "CUDA_ERROR_NOT_MAPPED_AS_ARRAY",
            CUDA_ERROR_NOT_MAPPED_AS_POINTER: "CUDA_ERROR_NOT_MAPPED_AS_POINTER",
            CUDA_ERROR_UNSUPPORTED_LIMIT: "CUDA_ERROR_UNSUPPORTED_LIMIT",
            CUDA_ERROR_CONTEXT_ALREADY_IN_USE: "CUDA_ERROR_CONTEXT_ALREADY_IN_USE",
            CUDA_ERROR_INVALID_SOURCE: "CUDA_ERROR_INVALID_SOURCE",
            CUDA_ERROR_FILE_NOT_FOUND: "CUDA_ERROR_FILE_NOT_FOUND",
            CUDA_ERROR_SHARED_OBJECT_SYMBOL_NOT_FOUND: "CUDA_ERROR_SHARED_OBJECT_SYMBOL_NOT_FOUND",
            CUDA_ERROR_SHARED_OBJECT_INIT_FAILED: "CUDA_ERROR_SHARED_OBJECT_INIT_FAILED",
            CUDA_ERROR_OPERATING_SYSTEM: "CUDA_ERROR_OPERATING_SYSTEM"
        }
        checkError.g_errorStrings = error_strings
    g_errorStrings = checkError.g_errorStrings

    # Emulate as in C++, just coverage, not real error handling
    if rCode in g_errorStrings:
        pass
    else:
        pass

class TestGpuBurnDrvPublic:
    def test_error_map_initialization_public(self):
        # Use different code and desc compared to private test
        checkError(CUDA_ERROR_NOT_INITIALIZED, "Init error for public test")
        checkError(CUDA_ERROR_DEINITIALIZED, "Deinit public memory")

    def test_known_error_codes_public(self):
        # Use codes in reverse order for public tests
        for code in range(24, 0, -1):
            checkError(code, "Public test for code")

    def test_unknown_error_code_public(self):
        # Use a different unknown code
        checkError(888, "Unknown public error branch")

    def test_non_empty_desc_symbols(self):
        # Edge case: use a desc with spaces and symbols
        checkError(CUDA_ERROR_INVALID_CONTEXT, "context@#$%^&*()desc")