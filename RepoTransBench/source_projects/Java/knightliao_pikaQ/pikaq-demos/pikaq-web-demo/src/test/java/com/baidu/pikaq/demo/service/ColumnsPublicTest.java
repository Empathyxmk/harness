package com.baidu.pikaq.demo.service;

import org.junit.Test;
import static org.junit.Assert.*;

public class ColumnsPublicTest {
    @Test
    public void testNameConstantNotNull() {
        assertNotNull(Columns.NAME);
        assertTrue(Columns.NAME.length() > 2); // Confirm length as different data than strict value
    }

    @Test
    public void testCampaignIdConstantHasId() {
        assertTrue(Columns.CAMPAIGN_ID.endsWith("Id"));
    }
}