package com.myshop.order;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class NoOrderExceptionTest {

    @Test
    void defaultConstructorSetsNoMessageOrCause() {
        NoOrderException ex = new NoOrderException();
        assertNull(ex.getMessage());
        assertNull(ex.getCause());
    }
}