package com.baidu.pikaq.demo.service.campaign.service.impl;

import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

import com.baidu.pikaq.client.producer.gateway.PikaQGateway;
import com.baidu.pikaq.client.producer.gateway.RabbitQGateway;
import com.baidu.pikaq.demo.service.campaign.dao.CampaignDao;
import com.baidu.pikaq.demo.service.campaign.bo.Campaign;
import com.baidu.pikaq.demo.service.campaign.message.MessageConstants;
import com.baidu.pikaq.demo.service.campaign.message.CampaignPikaMessageConverter;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;

public class CampaignMgrImplTest {

    private CampaignMgrImpl mgr;
    private PikaQGateway pikaQGateway;
    private RabbitQGateway rabbitQGateway;
    private CampaignDao campaignDao;

    @Before
    public void setUp() {
        pikaQGateway = mock(PikaQGateway.class);
        rabbitQGateway = mock(RabbitQGateway.class);
        campaignDao = mock(CampaignDao.class);
        mgr = new CampaignMgrImpl();
        // inject mocks
        mgr.pikaQGateway = pikaQGateway;
        mgr.rabbitQGateway = rabbitQGateway;
        mgr.campaignDao = campaignDao;
    }

    @Test
    public void testGetByName() {
        Campaign c = new Campaign();
        when(campaignDao.getByName("x")).thenReturn(c);
        assertSame(c, mgr.getByName("x"));
        verify(campaignDao).getByName("x");
    }

    @Test
    public void testFindAll() {
        List<Campaign> cs = Arrays.asList(new Campaign(), new Campaign());
        when(campaignDao.findAll()).thenReturn(cs);
        assertSame(cs, mgr.findAll());
        verify(campaignDao).findAll();
    }

    @Test
    public void testCreate() {
        Campaign c = new Campaign();
        when(campaignDao.create(anyString(), any())).thenReturn(c);

        Campaign result = mgr.create("foo", BigDecimal.valueOf(19));
        assertSame(c, result);

        verify(campaignDao).create(eq("foo"), eq(BigDecimal.valueOf(19)));
        verify(pikaQGateway).send(eq(MessageConstants.DEFAULT_EXCHANGE), eq(MessageConstants.DEFAULT_ROUTE_KEY),
                any());
    }

    @Test
    public void testCreateWithConsumerErrorPikaQStrong() {
        Campaign c = new Campaign();
        when(campaignDao.create(anyString(), any())).thenReturn(c);

        try {
            mgr.createWithConsumerErrorPikaQStrong("foo", BigDecimal.TEN);
            fail();
        } catch (RuntimeException e) {
            assertTrue(e.getMessage().contains("something wrong"));
        }
        verify(pikaQGateway).send(eq(MessageConstants.DEFAULT_EXCHANGE),
                eq(MessageConstants.ROUTE_KEY_CONSUMER_ERROR), any());
    }

    @Test
    public void testCreateWithConsumerErrorPikaQNormal() {
        Campaign c = new Campaign();
        when(campaignDao.create(anyString(), any())).thenReturn(c);

        try {
            mgr.createWithConsumerErrorPikaQNormal("f", BigDecimal.ONE);
            fail();
        } catch (RuntimeException e) {
            assertTrue(e.getMessage().contains("something wrong"));
        }
        verify(pikaQGateway).sendSimple(eq(MessageConstants.DEFAULT_EXCHANGE),
                eq(MessageConstants.ROUTE_KEY_CONSUMER_ERROR), any());
    }

    @Test
    public void testCreateWithConsumerError() {
        Campaign c = new Campaign();
        when(campaignDao.create(anyString(), any())).thenReturn(c);

        try {
            mgr.createWithConsumerError("abc", BigDecimal.ZERO);
            fail();
        } catch (RuntimeException e) {
            assertTrue(e.getMessage().contains("something wrong"));
        }
        verify(rabbitQGateway).send(eq(MessageConstants.DEFAULT_EXCHANGE),
                eq(MessageConstants.ROUTE_KEY_CONSUMER_ERROR), any());
    }

    @Test
    public void testUpdate_found() {
        Campaign c = new Campaign();
        when(campaignDao.get(anyLong())).thenReturn(c);

        mgr.update(22L, BigDecimal.valueOf(33));
        verify(campaignDao).updatePriceById(22L, BigDecimal.valueOf(33));
        assertEquals(BigDecimal.valueOf(33), c.getPrice());
        verify(pikaQGateway).sendSimple(eq(MessageConstants.DEFAULT_EXCHANGE),
                eq(MessageConstants.ROUTE_KEY2), any());
    }

    @Test
    public void testUpdate_notFound() {
        when(campaignDao.get(anyLong())).thenReturn(null);

        mgr.update(33L, BigDecimal.valueOf(12));
        verify(campaignDao).get(33L);
        verify(campaignDao, never()).updatePriceById(anyLong(), any());
        verify(pikaQGateway, never()).sendSimple(anyString(), anyString(), any());
    }
}