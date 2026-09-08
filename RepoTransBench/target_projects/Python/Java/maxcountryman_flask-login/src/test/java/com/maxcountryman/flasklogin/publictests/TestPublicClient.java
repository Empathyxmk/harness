package com.maxcountryman.flasklogin.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.maxcountryman.flasklogin.testclient.FlaskLoginClient;

public class TestPublicClient {

    static class DummyUser implements FlaskLoginClient.UserLike {
        private final String id;
        public DummyUser(Object id) { this.id = id.toString(); }
        @Override
        public String getId() { return id; }
    }

    @Test
    public void testFlaskLoginClientSetsUserIdPublic() {
        DummyUser u = new DummyUser("U987");
        FlaskLoginClient client = new FlaskLoginClient(u, false);
        assertEquals("U987", client.session.get("_user_id"));
        assertFalse((Boolean)client.session.get("_fresh"));
    }

    @Test
    public void testFlaskLoginClientNoUserPublic() {
        FlaskLoginClient client = new FlaskLoginClient();
        assertFalse(client.session.containsKey("_user_id"));
        assertFalse(client.session.containsKey("_fresh"));
    }
}