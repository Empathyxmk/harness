package com.maxcountryman.flasklogin.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.maxcountryman.flasklogin.mixins.UserMixin;
import com.maxcountryman.flasklogin.mixins.AnonymousUserMixin;

public class TestPublicMixins {
    static class User implements UserMixin {
        public Object id;
        User(Object id) { this.id = id; }
        @Override
        public Object getIdRaw() { return id; }
    }

    @Test
    public void testUserMixinIsActive() {
        User user = new User(100);
        assertTrue(user.isActive());
    }

    @Test
    public void testUserMixinIsAuthenticated() {
        User user = new User(200);
        assertTrue(user.isAuthenticated());
    }

    @Test
    public void testUserMixinIsAnonymous() {
        User user = new User(300);
        assertFalse(user.isAnonymous());
    }

    @Test
    public void testUserMixinGetIdReturnsStr() {
        User user = new User(456);
        assertEquals("456", user.getId());
        User user2 = new User("xyz");
        assertEquals("xyz", user2.getId());
    }

    @Test
    public void testUserMixinGetIdAttributeError() {
        User user = new User(null);
        assertThrows(
            com.maxcountryman.flasklogin.mixins.NotImplementedException.class,
            user::getId
        );
    }

    @Test
    public void testUserMixinEqTrue() {
        User user1 = new User(55);
        User user2 = new User(55);
        assertEquals(user1, user2);
    }

    @Test
    public void testUserMixinEqFalse() {
        User user1 = new User(11);
        User user2 = new User(12);
        assertNotEquals(user1, user2);
    }

    @Test
    public void testUserMixinEqType() {
        User user = new User(222);
        assertFalse(user.equals(new Object[]{}));
    }

    @Test
    public void testUserMixinNeType() {
        User user = new User(1234);
        assertTrue(!user.equals(null));
    }

    @Test
    public void testUserMixinHash() {
        User user = new User(42);
        assertTrue(Integer.class.isInstance(user.hashCode()) || int.class.isInstance(user.hashCode()));
    }

    @Test
    public void testAnonymousUserMixinProperties() {
        AnonymousUserMixin anon = new AnonymousUserMixin();
        assertFalse(anon.isActive());
        assertFalse(anon.isAuthenticated());
        assertTrue(anon.isAnonymous());
    }

    @Test
    public void testAnonymousUserMixinGetId() {
        AnonymousUserMixin anon = new AnonymousUserMixin();
        assertNull(anon.getId());
    }
}