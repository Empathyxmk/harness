package com.birin.gridlistviewadapters;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Public test for Card.
 */
public class CardPublicTest {

    @Test
    void testSetAndGetIdPublic() {
        Card card = new Card();
        card.setId(99L); // different from original value
        assertEquals(99L, card.getId());
    }

    @Test
    void testSetAndGetIsEnabledPublic() {
        Card card = new Card();
        card.setIsEnabled(false); // different value
        assertFalse(card.isEnabled());
    }

    @Test
    void testSetAndGetItemPublic() {
        Card card = new Card();
        Object item = "publicTestObject";
        card.setItem(item);
        assertEquals("publicTestObject", card.getItem());
    }
}