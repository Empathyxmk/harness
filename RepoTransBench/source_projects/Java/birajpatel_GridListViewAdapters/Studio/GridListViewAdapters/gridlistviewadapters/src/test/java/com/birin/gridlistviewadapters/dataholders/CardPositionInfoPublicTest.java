package com.birin.gridlistviewadapters.dataholders;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CardPositionInfoPublicTest {

    @Test
    public void testSetAndGetRowAndColumnPublic() {
        CardPositionInfo info = new CardPositionInfo();
        info.setRow(7);
        info.setColumn(8);
        assertEquals(7, info.getRow());
        assertEquals(8, info.getColumn());
    }
}