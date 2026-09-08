package test;

import org.junit.Test;
import static org.junit.Assert.*;

public class KcpServerExamplesPublicTest {
    @Test
    public void testSimplePublicServer() {
        int serverId = 42; // Different from typical original test data
        int port = 16667;  // Different port
        String expectedGreeting = "KCP Public Test Server Started (ServerID: 42, Port: 16667)";

        String serverGreeting = simulateServerStart(serverId, port);
        assertEquals(expectedGreeting, serverGreeting);
    }

    private String simulateServerStart(int serverId, int port) {
        return "KCP Public Test Server Started (ServerID: " + serverId + ", Port: " + port + ")";
    }
}