package com.example.public.show_pytest_warnings;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThatThrownBy;

class PublicFoobarShowWarningTest {
    @Test
    void testPublicWarningIsShown() {
        assertThatThrownBy(() -> {
            throw new UserWarning("this is a public test warning!");
        }).isInstanceOf(UserWarning.class)
        .hasMessageContaining("public test warning");
    }

    static class UserWarning extends RuntimeException {
        public UserWarning(String msg) {
            super(msg);
        }
    }
}