package com.birin.gridlistviewadapters.dataholders;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class RowDataHolderTest {
    @Test
    public void testRowDataHolder() {
        RowDataHolder holder = new RowDataHolder(0, 1);
        assertEquals(0, holder.rowNum);
        assertEquals(1, holder.numOfColumns);
    }
}