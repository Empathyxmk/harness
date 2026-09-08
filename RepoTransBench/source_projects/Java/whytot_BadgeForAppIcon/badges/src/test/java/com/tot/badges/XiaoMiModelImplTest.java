package com.tot.badges;

import android.app.Application;
import android.app.Notification;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.fail;

public class XiaoMiModelImplTest {

    private XiaoMiModelImpl xiaoMiModel;

    @Mock
    Application mockApplication;

    // A dummy Notification class that mimics the structure XiaoMiModelImpl expects via reflection
    static class TestNotification extends Notification {
        public TestExtraNotification extraNotification = new TestExtraNotification();

        static class TestExtraNotification {
            private int messageCount = 0;

            public void setMessageCount(int count) {
                this.messageCount = count;
            }

            public int getMessageCount() {
                return messageCount;
            }
        }
    }

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        xiaoMiModel = new XiaoMiModelImpl();
    }

    @Test
    public void testSetIconBadgeNum_nullNotification() {
        try {
            xiaoMiModel.setIconBadgeNum(mockApplication, null, 10);
            fail("Expected an Exception for null notification");
        } catch (Exception e) {
            assertEquals("Xiaomi phones must send notification", e.getMessage());
        }
    }

    @Test
    public void testSetIconBadgeNum_validNotification() throws Exception {
        TestNotification notification = new TestNotification();
        int testCount = 5;

        Notification result = xiaoMiModel.setIconBadgeNum(mockApplication, notification, testCount);

        assertNotNull(result);
        assertSame(notification, result);
        assertEquals(testCount, notification.extraNotification.getMessageCount());
    }
}