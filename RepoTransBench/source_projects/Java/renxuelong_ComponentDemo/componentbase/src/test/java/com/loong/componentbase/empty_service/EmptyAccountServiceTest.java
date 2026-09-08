package com.loong.componentbase.empty_service;

import com.loong.componentbase.service.IAccountService;
import org.junit.Test;
import static org.junit.Assert.*;

public class EmptyAccountServiceTest {

    @Test
    public void testIsLoginIsFalse() {
        IAccountService service = new EmptyAccountService();
        assertFalse(service.isLogin());
    }

    @Test
    public void testGetAccountIdIsNull() {
        IAccountService service = new EmptyAccountService();
        assertNull(service.getAccountId());
    }

    @Test
    public void testNewUserFragmentIsNull() {
        IAccountService service = new EmptyAccountService();
        assertNull(service.newUserFragment(null, 0, null, null, null));
    }
}