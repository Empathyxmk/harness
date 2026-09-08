package com.birin.gridlistviewadapters.dataholders;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CardDataHolderTest {
    @Test
    public void testCardDataHolder() {
        CardDataHolder holder = new CardDataHolder("text", 1, 2, false, 0);
        assertEquals("text", holder.text);
        assertEquals(1, holder.cardType);
        assertEquals(2, holder.position);
        assertFalse(holder.isHeaderOrFooter);
        assertEquals(0, holder.viewType);
    }
}