package com.baidu.pikaq.demo.service;

import org.junit.Test;
import static org.junit.Assert.*;

public class ColumnsTest {
    @Test
    public void testNameConstant() {
        assertEquals("name", Columns.NAME);
    }

    @Test
    public void testCampaignIdConstant() {
        assertEquals("campaignId", Columns.CAMPAIGN_ID);
    }
}