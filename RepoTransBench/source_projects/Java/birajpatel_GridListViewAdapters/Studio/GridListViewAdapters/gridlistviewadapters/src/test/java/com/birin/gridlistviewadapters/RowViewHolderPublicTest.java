package com.birin.gridlistviewadapters;

import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Public test for RowViewHolder - using different items.
 */
class RowViewHolderPublicTest {
    @Test
    void testGetCardViewHoldersInitialEmptyPublic() {
        RowViewHolder<Integer> holder = new RowViewHolder<>();
        ArrayList<Integer> l = holder.getCardViewHolders();
        assertNotNull(l);
        assertTrue(l.isEmpty());
    }

    @Test
    void testAddItemToCardViewHoldersPublic() {
        RowViewHolder<Integer> holder = new RowViewHolder<>();
        holder.getCardViewHolders().add(12345);
        assertEquals(1, holder.getCardViewHolders().size());
        assertEquals(Integer.valueOf(12345), holder.getCardViewHolders().get(0));
    }
}