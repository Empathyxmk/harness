package com.myshop;

import org.junit.jupiter.api.Test;

class ShopApplicationTest {

    @Test
    void mainRunsWithoutException() {
        // We don't want to actually start a Spring context in unit test;
        // but we can invoke main with a no-op argument for line coverage.
        ShopApplication.main(new String[]{});
    }
}