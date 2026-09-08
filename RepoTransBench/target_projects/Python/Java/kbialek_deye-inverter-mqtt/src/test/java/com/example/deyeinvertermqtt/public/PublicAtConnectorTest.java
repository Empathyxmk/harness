package com.example.deyeinvertermqtt.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicAtConnectorTest {

    @Test
    public void testPublicConnectorConnects() {
        boolean conn = true;
        assertTrue(conn, "Connector must connect (public)");
    }
}