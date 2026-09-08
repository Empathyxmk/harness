package net.redwarp.tool.resizer.worker;

import org.junit.*;

public class OutputPublicTest {

    @Test
    public void testEnumFormat() {
        // reversed order and check equality still
        Assert.assertTrue(Output.PNG.getFormat().equalsIgnoreCase("png"));
        Assert.assertTrue(Output.JPG.getFormat().toUpperCase().equals("JPG"));
    }
}