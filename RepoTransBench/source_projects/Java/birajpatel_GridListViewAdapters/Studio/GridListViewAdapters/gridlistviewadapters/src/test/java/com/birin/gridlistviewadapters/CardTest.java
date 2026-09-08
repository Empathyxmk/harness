package com.birin.gridlistviewadapters;

import android.view.View;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class CardTest {
    static class DummyVH {}

    @Test
    void testCardCreationAndGetters() {
        View v = mock(View.class);
        DummyVH vh = new DummyVH();

        Card<DummyVH> card = new Card<>(v, vh);

        assertSame(v, card.getCardView());
        assertSame(vh, card.getCardViewHolder());
    }
}