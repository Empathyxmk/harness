package com.medium.sdk.public_tests;

import com.medium.sdk.Client;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestClientPublicExtra {

    @Test
    public void testClientInitPublic() {
        Client c = new Client("public_token_abc");
        assertEquals("public_token_abc", c.token);
    }
}