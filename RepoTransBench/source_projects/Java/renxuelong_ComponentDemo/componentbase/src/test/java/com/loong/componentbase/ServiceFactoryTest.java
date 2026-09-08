package com.loong.componentbase;

import com.loong.componentbase.empty_service.EmptyAccountService;
import com.loong.componentbase.service.IAccountService;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class ServiceFactoryTest {

    @Before
    public void setUp() {
        // Reset state for singletons before each test if necessary
        ServiceFactory.getInstance().setAccountService(null);
    }

    @Test
    public void testSingletonInstance() {
        ServiceFactory factory1 = ServiceFactory.getInstance();
        ServiceFactory factory2 = ServiceFactory.getInstance();
        assertSame(factory1, factory2);
    }

    @Test
    public void testSetAndGetAccountService() {
        MockAccountService mockService = new MockAccountService();
        ServiceFactory.getInstance().setAccountService(mockService);
        IAccountService result = ServiceFactory.getInstance().getAccountService();
        assertSame(mockService, result);
    }

    @Test
    public void testGetAccountServiceReturnsEmptyIfNull() {
        ServiceFactory.getInstance().setAccountService(null);
        IAccountService service = ServiceFactory.getInstance().getAccountService();
        assertNotNull(service);
        assertTrue(service instanceof EmptyAccountService);
    }

    private static class MockAccountService implements IAccountService {
        @Override public boolean isLogin() { return true; }
        @Override public String getAccountId() { return "mock"; }
        @Override public android.support.v4.app.Fragment newUserFragment(
                android.app.Activity activity, int containerId,
                android.support.v4.app.FragmentManager manager,
                android.os.Bundle bundle, String tag
        ) { return null; }
    }
}