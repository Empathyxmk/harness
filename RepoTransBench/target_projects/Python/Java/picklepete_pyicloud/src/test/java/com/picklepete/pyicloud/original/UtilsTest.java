package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.mockito.Mockito;

import com.picklepete.pyicloud.utils.*;
import com.picklepete.pyicloud.exceptions.PyiCloudNoStoredPasswordAvailableException;

import java.lang.reflect.Field;

class DummyKeyring {
    public java.util.Map<String, String> saved = new java.util.HashMap<>();
    public java.util.List<String> deleted = new java.util.ArrayList<>();
    public String getPassword(String system, String username) {
        return saved.get(username);
    }
    public String setPassword(String system, String username, String password) {
        saved.put(username, password);
        return "set";
    }
    public String deletePassword(String system, String username) {
        deleted.add(username);
        return "del";
    }
}

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class UtilsTest {

    DummyKeyring dkr;

    @BeforeEach
    public void patchKeyring() throws Exception {
        dkr = new DummyKeyring();
        // Patch keyring in utils
        Field f = Utils.class.getDeclaredField("keyring");
        f.setAccessible(true);
        f.set(null, dkr);
    }

    @Test
    public void testGetPasswordFromKeyringSuccess() {
        dkr.saved.put("foo", "bar");
        assertEquals("bar", Utils.getPasswordFromKeyring("foo"));
    }

    @Test
    public void testGetPasswordFromKeyringFailure() {
        assertThrows(PyiCloudNoStoredPasswordAvailableException.class, () -> Utils.getPasswordFromKeyring("not-exist"));
    }

    @Test
    public void testPasswordExistsInKeyringTrue() {
        dkr.saved.put("a", "b");
        assertTrue(Utils.passwordExistsInKeyring("a"));
    }

    @Test
    public void testPasswordExistsInKeyringFalse() {
        assertFalse(Utils.passwordExistsInKeyring("none"));
    }

    @Test
    public void testStorePasswordInKeyring() {
        String result = Utils.storePasswordInKeyring("x", "y");
        assertEquals("y", dkr.saved.get("x"));
        assertEquals("set", result);
    }

    @Test
    public void testDeletePasswordInKeyring() {
        dkr.saved.put("delme", "foo");
        String result = Utils.deletePasswordInKeyring("delme");
        assertTrue(dkr.deleted.contains("delme"));
        assertEquals("del", result);
    }

    @Test
    public void testUnderscoreToCamelcaseBasic() {
        assertEquals("helloWorld", Utils.underscoreToCamelcase("hello_world", false));
        assertEquals("AB", Utils.underscoreToCamelcase("A_b", true));
    }

    @Test
    public void testGetPasswordInteractiveFalse() throws Exception {
        Utils.setGetPasswordFromKeyringImpl(username -> { throw new PyiCloudNoStoredPasswordAvailableException(); });
        assertThrows(PyiCloudNoStoredPasswordAvailableException.class, () -> Utils.getPassword("z", false));
    }

    @Test
    public void testGetPasswordInteractiveTrue() throws Exception {
        Utils.setGetPasswordFromKeyringImpl(username -> { throw new PyiCloudNoStoredPasswordAvailableException(); });
        Utils.setGetPassImpl(prompt -> "foo");
        String out = Utils.getPassword("z", true);
        assertEquals("foo", out);
    }
}