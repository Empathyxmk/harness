package com.packtpublishing.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestEchoServerTest {

    String echo(String in) {
        return in;
    }

    @Test
    void testEchoNormal() {
        assertEquals("hello world", echo("hello world"));
        assertEquals("12345", echo("12345"));
    }

    @Test
    void testEchoSpecial() {
        assertEquals("测试", echo("测试"));
    }

    @Test
    void testEchoWhitespace() {
        assertEquals(" ", echo(" "));
        assertEquals("\t\n", echo("\t\n"));
    }
}