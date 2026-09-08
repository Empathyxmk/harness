package com.birin.gridlistviewadapters.utils;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MaxCardsInfoPublicTest {
    @Test
    void testSetAndGetMaxCardsPerRowPublic() {
        MaxCardsInfo info = new MaxCardsInfo();
        info.setMaxCardsPerRow(6);
        assertEquals(6, info.getMaxCardsPerRow());
    }
}