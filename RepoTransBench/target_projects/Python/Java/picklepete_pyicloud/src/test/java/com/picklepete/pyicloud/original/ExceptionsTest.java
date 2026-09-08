package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.picklepete.pyicloud.exceptions.*;

public class ExceptionsTest {

    @Test
    public void testPyiCloudException() {
        PyiCloudException ex = new PyiCloudException("test");
        assertTrue(ex instanceof Exception);
        assertEquals("test", ex.getMessage());
    }

    @Test
    public void testPyiCloudAPIResponseExceptionBasic() {
        PyiCloudAPIResponseException ex = new PyiCloudAPIResponseException("error reason");
        assertTrue(ex.getMessage().contains("error reason"));
        assertEquals("error reason", ex.getReason());
        assertNull(ex.getCode());
    }

    @Test
    public void testPyiCloudAPIResponseExceptionFull() {
        PyiCloudAPIResponseException ex = new PyiCloudAPIResponseException("fail", "42", true);
        String s = ex.toString();
        assertTrue(s.contains("fail") && s.contains("42") && s.contains("Retrying"));
        assertEquals("fail", ex.getReason());
        assertEquals("42", ex.getCode());
    }

    @Test
    public void testServiceNotActivatedException() {
        PyiCloudServiceNotActivatedException ex = new PyiCloudServiceNotActivatedException("reason");
        assertTrue(ex.getMessage().contains("reason"));
    }

    @Test
    public void testFailedLoginException() {
        PyiCloudFailedLoginException ex = new PyiCloudFailedLoginException("login fail");
        assertTrue(ex.getMessage().contains("login fail"));
    }

    @Test
    public void test2SARequiredException() {
        PyiCloud2SARequiredException ex = new PyiCloud2SARequiredException("email@email.com");
        assertTrue(ex.getMessage().contains("Two-step authentication required for account: email@email.com"));
    }

    @Test
    public void testNoStoredPasswordException() {
        PyiCloudNoStoredPasswordAvailableException ex = new PyiCloudNoStoredPasswordAvailableException("no password");
        assertTrue(ex.getMessage().contains("no password"));
    }

    @Test
    public void testNoDevicesException() {
        PyiCloudNoDevicesException ex = new PyiCloudNoDevicesException("no device");
        assertTrue(ex.getMessage().contains("no device"));
    }
}