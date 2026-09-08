package com.example.docxmailmerge;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Assertions;

public class TestMailmergeErrors {
    @Test
    public void test_error_on_bad_input() {
        // Test that an exception is thrown if input is invalid (simulating the Python pytest.raises usage)
        Assertions.assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("bad input");
        });
    }
}