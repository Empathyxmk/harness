package com.maxcountryman.flasklogin.original;

import com.maxcountryman.flasklogin.login.LoginManager;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestLoginManager {

    @Test
    public void testInstanceDefaults() {
        LoginManager lm = new LoginManager();
        assertNotNull(lm.anonymousUser);
        assertNull(lm.loginView);
        assertTrue(lm.blueprintLoginViews instanceof java.util.Map);
        assertTrue(lm.loginMessageCategory.contains("message"));
        assertTrue(lm.needsRefreshMessage.toLowerCase().contains("refresh"));
        assertEquals("get_id", lm.idAttribute);
        assertTrue(lm.sessionProtection == null || lm.sessionProtection.equals("basic") || lm.sessionProtection.equals("strong"));
    }

    @Test
    public void testLoginManagerCustomValues() {
        LoginManager lm = new LoginManager();
        lm.setLoginView("/custom_login");
        lm.setRefreshView("/refresh_needed");
        lm.setLoginMessage("You must sign in!");
        lm.blueprintLoginViews.put("bp2", "/bp2_custom_login");
        assertTrue(lm.loginView.startsWith("/"));
        assertTrue(lm.refreshView.endsWith("needed"));
        assertTrue(lm.loginMessage.contains("sign in"));
        assertTrue(lm.blueprintLoginViews.get("bp2").startsWith("/bp2"));
        lm.sessionProtection = "strong";
        assertEquals("strong", lm.sessionProtection);
    }

    @Test
    public void testLoginManagerAnonymousUser() {
        LoginManager lm = new LoginManager();
        class CustomAnon {}
        lm.anonymousUser = CustomAnon.class;
        assertEquals(CustomAnon.class, lm.anonymousUser);
    }

    @Test
    public void testLocalizeCallback() {
        LoginManager lm = new LoginManager();
        final String[] called = {null};
        class Localizer {
            void localize(String val) { called[0] = val; }
        }
        Localizer l = new Localizer();
        lm.setLocalizeCallback(l);
        ((Localizer)lm.localizeCallback).localize("hello");
        assertEquals("hello", called[0]);
    }
}