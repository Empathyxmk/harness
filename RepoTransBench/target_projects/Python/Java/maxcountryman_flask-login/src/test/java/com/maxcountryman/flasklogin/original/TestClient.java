package com.maxcountryman.flasklogin.original;

import com.maxcountryman.flasklogin.testclient.FlaskLoginClient;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestClient {

    static class DummyUser implements FlaskLoginClient.UserLike {
        private final String id;
        public DummyUser(Object id) { this.id = id.toString(); }
        @Override
        public String getId() { return id; }
    }

    @Test
    public void testFlaskLoginClientSetsUserId() {
        DummyUser u = new DummyUser("U123");
        FlaskLoginClient client = new FlaskLoginClient(u, false);
        assertEquals("U123", client.session.get("_user_id"));
        assertFalse((Boolean)client.session.get("_fresh"));
    }

    @Test
    public void testFlaskLoginClientNoUser() {
        FlaskLoginClient client = new FlaskLoginClient();
        assertFalse(client.session.containsKey("_user_id"));
        assertFalse(client.session.containsKey("_fresh"));
    }
}