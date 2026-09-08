package org.cyclopsgroup.jmxterm.io;

import org.junit.Test;

import java.io.ByteArrayInputStream;
import java.io.IOException;

import static org.junit.Assert.*;

public class InputStreamCommandInputPublicTest {

    @Test
    public void testReadLineFromInputStream() throws IOException {
        String data = "Delta\nEpsilon\n";
        ByteArrayInputStream bais = new ByteArrayInputStream(data.getBytes());
        InputStreamCommandInput input = new InputStreamCommandInput(bais);

        assertEquals("Delta", input.readLine());
        assertEquals("Epsilon", input.readLine());
        assertNull(input.readLine());
        input.close();
    }
}