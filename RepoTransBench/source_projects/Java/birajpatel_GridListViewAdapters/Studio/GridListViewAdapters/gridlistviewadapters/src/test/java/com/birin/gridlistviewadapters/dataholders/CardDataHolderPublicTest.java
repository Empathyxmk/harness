package com.birin.gridlistviewadapters.dataholders;

import com.birin.gridlistviewadapters.dataholders.CardDataHolder;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CardDataHolderPublicTest {

    @Test
    public void testSetAndGetCardIdPublic() {
        CardDataHolder holder = new CardDataHolder();
        holder.setCardId(808L); // different id
        assertEquals(808L, holder.getCardId());
    }

    @Test
    public void testSetAndGetIsEnabledPublic() {
        CardDataHolder holder = new CardDataHolder();
        holder.setIsEnabled(false);
        assertFalse(holder.isEnabled());
    }

    @Test
    public void testSetAndGetCardPublic() {
        CardDataHolder holder = new CardDataHolder();
        Object card = "testPublicCard";
        holder.setCard(card);
        assertEquals("testPublicCard", holder.getCard());
    }
}