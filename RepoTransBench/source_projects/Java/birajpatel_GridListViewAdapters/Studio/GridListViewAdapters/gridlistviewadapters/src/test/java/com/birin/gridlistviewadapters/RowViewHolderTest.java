package com.birin.gridlistviewadapters;

import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import static org.junit.jupiter.api.Assertions.*;

class RowViewHolderTest {
    @Test
    void testGetCardViewHoldersInitialEmpty() {
        RowViewHolder<String> holder = new RowViewHolder<>();
        ArrayList<String> l = holder.getCardViewHolders();
        assertNotNull(l);
        assertTrue(l.isEmpty());
    }

    @Test
    void testAddItemToCardViewHolders() {
        RowViewHolder<String> holder = new RowViewHolder<>();
        holder.getCardViewHolders().add("abc");
        assertEquals(1, holder.getCardViewHolders().size());
        assertEquals("abc", holder.getCardViewHolders().get(0));
    }
}