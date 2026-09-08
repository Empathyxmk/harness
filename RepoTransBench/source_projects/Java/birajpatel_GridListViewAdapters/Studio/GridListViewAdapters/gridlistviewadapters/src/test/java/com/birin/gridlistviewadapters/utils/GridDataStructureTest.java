package com.birin.gridlistviewadapters.utils;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

import java.util.Arrays;
import java.util.List;

public class GridDataStructureTest {

    private GridDataStructure<String> gridData;

    @Before
    public void setUp() {
        List<String> list = Arrays.asList("A", "B", "C", "D", "E");
        gridData = new GridDataStructure<>(list, 2);
    }

    @Test
    public void testGetRowCount() {
        assertEquals(3, gridData.getRowCount());
    }

    @Test
    public void testGetDataForRow() {
        List<String> row = gridData.getDataForRow(1);
        assertEquals(Arrays.asList("C", "D"), row);
    }

    @Test
    public void testGetDataForLastRow() {
        List<String> row = gridData.getDataForRow(2);
        assertEquals(Arrays.asList("E"), row);
    }

    @Test(expected = IndexOutOfBoundsException.class)
    public void testGetDataForRow_invalid() {
        gridData.getDataForRow(6);
    }
}