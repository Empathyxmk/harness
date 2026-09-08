package com.maxcountryman.flasklogin.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.maxcountryman.flasklogin.mixins.UserMixin;
import com.maxcountryman.flasklogin.mixins.AnonymousUserMixin;

public class TestMixins {

    static class User implements UserMixin {
        public Object id;
        User(Object id) { this.id = id; }
        @Override
        public Object getIdRaw() { return id; }
    }

    @Test
    public void testUserMixinIsActive() {
        User user = new User(1);
        assertTrue(user.isActive());
    }

    @Test
    public void testUserMixinIsAuthenticated() {
        User user = new User(2);
        assertTrue(user.isAuthenticated());
    }

    @Test
    public void testUserMixinIsAnonymous() {
        User user = new User(3);
        assertFalse(user.isAnonymous());
    }

    @Test
    public void testUserMixinGetIdReturnsStr() {
        User user = new User(123);
        assertEquals("123", user.getId());
        User user2 = new User("abc");
        assertEquals("abc", user2.getId());
    }

    @Test
    public void testUserMixinGetIdAttributeError() {
        User user = new User(1);
        user.id = null;
        assertThrows(
            com.maxcountryman.flasklogin.mixins.NotImplementedException.class,
            user::getId
        );
    }

    @Test
    public void testUserMixinEqTrue() {
        User user1 = new User(9);
        User user2 = new User(9);
        assertEquals(user1, user2);
    }

    @Test
    public void testUserMixinEqFalse() {
        User user1 = new User(1);
        User user2 = new User(2);
        assertNotEquals(user1, user2);
    }

    @Test
    public void testUserMixinEqType() {
        User user = new User(1);
        assertFalse(user.equals(new Object()));
    }

    @Test
    public void testUserMixinNeType() {
        User user = new User(1);
        assertTrue(!user.equals(new Object()));
    }

    @Test
    public void testUserMixinHash() {
        User user = new User(1);
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