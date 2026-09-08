package com.luckysj.demo.concurrent;

import com.luckysj.demo.entity.UserDO;
import com.luckysj.demo.model.request.UserReq;
import com.luckysj.demo.service.impl.UserServiceImpl;
import org.junit.Before;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.*;

public class UserServiceImplPublicTest {

    private UserServiceImpl userService;

    @Before
    public void setUp() {
        userService = new UserServiceImpl();
        // pre-populate with a different user for public test
        UserReq req = new UserReq();
        req.setUserName("publicuser");
        userService.add(req);
    }

    @Test
    public void testAddUser() {
        UserReq req = new UserReq();
        req.setUserName("bob");
        boolean result = userService.add(req);
        assertTrue(result);

        List<UserDO> users = userService.queryAll();
        boolean hasBob = users.stream().anyMatch(u -> "bob".equals(u.getUserName()));
        assertTrue(hasBob);
    }

    @Test
    public void testQueryAll() {
        List<UserDO> users = userService.queryAll();
        assertNotNull(users);
        assertFalse(users.isEmpty());
    }

    @Test
    public void testAddDuplicateUser() {
        UserReq req = new UserReq();
        req.setUserName("publicuser"); // publicuser is setup by @Before
        boolean result = userService.add(req);
        assertTrue(result);
    }
}