package com.typeerror.secure.original.headers;

import com.typeerror.secure.headers.Server;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestServer {

    @Test
    public void testDefaultServer() {
        Server serverHeader = new Server();
        assertEquals("", serverHeader.getHeaderValue());
    }

    @Test
    public void testSetCustomServer() {
        Server serverHeader = new Server().set("CustomServer");
        assertEquals("CustomServer", serverHeader.getHeaderValue());
    }

    @Test
    public void testClearServer() {
        Server serverHeader = new Server().set("CustomServer").clear();
        assertEquals("", serverHeader.getHeaderValue());
    }
}