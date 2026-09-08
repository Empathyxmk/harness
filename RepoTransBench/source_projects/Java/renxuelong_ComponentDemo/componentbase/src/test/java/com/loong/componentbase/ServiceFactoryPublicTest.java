package com.loong.componentbase;

import com.loong.componentbase.empty_service.EmptyAccountService;
import com.loong.componentbase.service.IAccountService;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class ServiceFactoryPublicTest {

    @Before
    public void setUp() {
        // Ensure fresh singleton state before each test
        ServiceFactory.getInstance().setAccountService(null);
    }

    @Test
    public void testSingletonInstancePublic() {
        ServiceFactory instance1 = ServiceFactory.getInstance();
        ServiceFactory instance2 = ServiceFactory.getInstance();
        assertSame(instance1, instance2);
    }

    @Test
    public void testSetAndGetDifferentMockAccountService() {
        DifferentMockAccountService service = new DifferentMockAccountService();
        ServiceFactory.getInstance().setAccountService(service);
        IAccountService result = ServiceFactory.getInstance().getAccountService();
        assertSame(service, result);
    }

    @Test
    public void testGetAccountServiceReturnsEmptyIfNullPublic() {
        ServiceFactory.getInstance().setAccountService(null);
        IAccountService service = ServiceFactory.getInstance().getAccountService();
        assertNotNull(service);
        assertTrue(service instanceof EmptyAccountService);
    }

    private static class DifferentMockAccountService implements IAccountService {
        @Override public boolean isLogin() { return false; } // differs from original (true in original)
        @Override public String getAccountId() { return "public_mock_id"; } // different value
        @Override public android.support.v4.app.Fragment newUserFragment(
                android.app.Activity activity, int containerId,
                android.support.v4.app.FragmentManager manager,
                android.os.Bundle bundle, String tag
        ) { return null; }
    }
}