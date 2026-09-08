package com.example.original.show_pytest_warnings;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThatThrownBy;

class FoobarShowWarningTest {
    @Test
    void testWarns() {
        // In Java, warnings are not "caught" like Python; use exception for test demonstration
        assertThatThrownBy(() -> {
            throw new UserWarning("this is a warning");
        }).isInstanceOf(UserWarning.class);
    }

    static class UserWarning extends RuntimeException {
        public UserWarning(String msg) {
            super(msg);
        }
    }
}