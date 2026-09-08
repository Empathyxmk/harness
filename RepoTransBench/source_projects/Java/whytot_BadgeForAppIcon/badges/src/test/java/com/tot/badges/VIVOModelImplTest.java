package com.tot.badges;

import android.app.Application;
import android.app.Notification;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

public class VIVOModelImplTest {

    private VIVOModelImpl vivoModel;

    @Mock
    Application mockApplication;
    @Mock
    Notification mockNotification;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        vivoModel = new VIVOModelImpl();
    }

    @Test
    public void testSetIconBadgeNum_alwaysThrowsException() {
        try {
            vivoModel.setIconBadgeNum(mockApplication, mockNotification, 10);
            fail("Expected an Exception for VIVO");
        } catch (Exception e) {
            assertEquals("not support : vivo", e.getMessage());
        }
    }
}