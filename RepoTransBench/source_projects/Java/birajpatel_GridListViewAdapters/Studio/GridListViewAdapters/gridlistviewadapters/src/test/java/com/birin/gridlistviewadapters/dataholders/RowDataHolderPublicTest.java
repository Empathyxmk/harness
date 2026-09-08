package com.birin.gridlistviewadapters.dataholders;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class RowDataHolderPublicTest {

    @Test
    public void testSetAndGetRowIdPublic() {
        RowDataHolder holder = new RowDataHolder();
        holder.setRowId(101L); // different value
        assertEquals(101L, holder.getRowId());
    }

    @Test
    public void testSetAndGetRowPublic() {
        RowDataHolder holder = new RowDataHolder();
        Object row = "PublicRow";
        holder.setRow(row);
        assertEquals("PublicRow", holder.getRow());
    }
}